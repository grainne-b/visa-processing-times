import csv
import re
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

URL = "https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times"
DATA_DIR = Path("data")
README_MD = Path("README.md")


# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------

def fetch_page_html() -> str:
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(8000)
        html = page.content()
        browser.close()
    return html


def parse_table(table) -> list[list[str]]:
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(separator=" ", strip=True) for td in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows


def find_section_table(soup, heading_text):
    heading = soup.find(lambda tag: tag.name == "h2" and heading_text.lower() in tag.get_text().lower())
    if not heading:
        return None, None
    section = heading.find_parent()
    while section and not section.find("table"):
        section = section.find_parent()
    paragraph = section.find("p") if section else None
    table = section.find("table") if section else None
    return paragraph, table


def extract_processing_times(soup) -> list[dict]:
    _, table = find_section_table(soup, "Processing times")
    if not table:
        return []

    rows = parse_table(table)
    if not rows:
        return []

    records = []
    last_app_type = ""
    for row in rows[1:]:
        # 6-cell rows include the application type in the first column
        if len(row) == 6:
            last_app_type = row[0]
            records.append({
                "application_type": row[0],
                "period_counted": row[1],
                "p25": row[2],
                "p50": row[3],
                "p75": row[4],
                "p90": row[5],
            })
        # 5-cell rows are sub-rows where the application type cell is merged above
        elif len(row) == 5:
            records.append({
                "application_type": last_app_type,
                "period_counted": row[0],
                "p25": row[1],
                "p50": row[2],
                "p75": row[3],
                "p90": row[4],
            })
    return records


def extract_applications_on_hand(soup) -> tuple[str, list[dict]]:
    paragraph, table = find_section_table(soup, "Number of applications we have")
    report_date = ""
    if paragraph:
        match = re.search(r"on\s+(\d{1,2}\s+\w+\s+\d{4})", paragraph.get_text())
        if match:
            report_date = match.group(1)

    if not table:
        return report_date, []

    rows = parse_table(table)
    records = []
    for row in rows[1:]:
        if len(row) >= 2:
            records.append({
                "report_date": report_date,
                "application_type": row[0],
                "count": row[1].replace(",", ""),
            })
    return report_date, records


def extract_applications_received(soup) -> tuple[str, str, list[dict]]:
    paragraph, table = find_section_table(soup, "Number of applications received")
    period_start, period_end = "", ""
    if paragraph:
        match = re.search(r"between\s+(\d{1,2}\s+\w+)\s+and\s+(\d{1,2}\s+\w+\s+\d{4})", paragraph.get_text())
        if match:
            year = re.search(r"\d{4}", match.group(2)).group()
            period_start = f"{match.group(1)} {year}"
            period_end = match.group(2)

    if not table:
        return period_start, period_end, []

    rows = parse_table(table)
    records = []
    for row in rows[1:]:
        if len(row) >= 2:
            records.append({
                "period_start": period_start,
                "period_end": period_end,
                "application_type": row[0],
                "count": row[1].replace(",", ""),
            })
    return period_start, period_end, records


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def append_csv(filepath: Path, fieldnames: list[str], rows: list[dict]):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    write_header = not filepath.exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def load_snapshots_by_date(csv_path: Path, date_field: str) -> dict[str, list[dict]]:
    """Read a CSV and group rows by date_field. Returns {date_str: [rows]}."""
    if not csv_path.exists():
        return {}
    snapshots: dict[str, list[dict]] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            date = row[date_field]
            snapshots.setdefault(date, []).append(row)
    return snapshots


def two_most_recent(snapshots: dict[str, list[dict]]) -> tuple[list[dict] | None, list[dict] | None]:
    """Return (previous, current) rows for the two most recent dates, or (None, current) if only one date exists."""
    if not snapshots:
        return None, None

    def parse_date(s):
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue
        return datetime.min

    sorted_dates = sorted(snapshots.keys(), key=parse_date)
    current = snapshots[sorted_dates[-1]]
    previous = snapshots[sorted_dates[-2]] if len(sorted_dates) >= 2 else None
    return previous, current


# ---------------------------------------------------------------------------
# Change display helpers
# ---------------------------------------------------------------------------

def parse_duration_days(value: str) -> int | None:
    """Convert '5 months' or '15 days' to approximate days for comparison."""
    match = re.match(r"(\d+)\s+(month|day)", value.strip(), re.IGNORECASE)
    if not match:
        return None
    n, unit = int(match.group(1)), match.group(2).lower()
    return n * 30 if unit == "month" else n


def duration_trend(old_val: str, new_val: str) -> str:
    """
    For processing times, lower is better (faster).
    Returns a symbol + label: '↓ faster', '↑ slower', '→ unchanged'.
    """
    old_days = parse_duration_days(old_val)
    new_days = parse_duration_days(new_val)
    if old_days is None or new_days is None or old_val == new_val:
        return "→ unchanged"
    if new_days < old_days:
        return "↓ faster"
    return "↑ slower"


def count_change(old_count: str, new_count: str) -> str:
    """
    Returns a formatted change string, e.g. '↓ -3,142 (-3.4%)' or '↑ +672 (+4.0%)'.
    """
    try:
        old, new = int(old_count), int(new_count)
    except ValueError:
        return "—"
    diff = new - old
    if old == 0:
        return "—"
    pct = (diff / old) * 100
    sign = "+" if diff >= 0 else ""
    arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "→")
    return f"{arrow} {sign}{diff:,} ({sign}{pct:.1f}%)"


def _short_app_type(app_type: str) -> str:
    """Shorten verbose application type labels for console display."""
    app_type = re.sub(r"\s*\d+$", "", app_type).strip()  # strip trailing footnote numbers
    if "conferral" in app_type.lower():
        return "By conferral"
    if "descent" in app_type.lower():
        return "By descent"
    if "evidence" in app_type.lower():
        return "Evidence"
    return app_type


# ---------------------------------------------------------------------------
# Console summary (Option A)
# ---------------------------------------------------------------------------

def print_change_summary(
    prev_processing: list[dict] | None,
    curr_processing: list[dict],
    prev_on_hand: list[dict] | None,
    curr_on_hand: list[dict],
    prev_received: list[dict] | None,
    curr_received: list[dict],
    prev_date: str,
    curr_date: str,
):
    print()
    print("=" * 60)
    if prev_date:
        print(f"  UPDATE DETECTED: {prev_date}  →  {curr_date}")
    else:
        print(f"  FIRST SNAPSHOT: {curr_date}")
    print("=" * 60)

    # Processing times
    print("\nProcessing Times (p90 — time by which 90% of applications are decided):")
    prev_pt = {(r["application_type"], r["period_counted"]): r for r in (prev_processing or [])}
    for r in curr_processing:
        key = (r["application_type"], r["period_counted"])
        label = f"  {_short_app_type(r['application_type'])} / {r['period_counted']}"
        if prev_pt and key in prev_pt:
            old_p90 = prev_pt[key]["p90"]
            trend = duration_trend(old_p90, r["p90"])
            print(f"{label:<55}  {old_p90:>10}  →  {r['p90']:<10}  {trend}")
        else:
            print(f"{label:<55}  {r['p90']}")

    # Applications on hand
    print("\nApplications on Hand:")
    prev_oh = {r["application_type"]: r for r in (prev_on_hand or [])}
    for r in curr_on_hand:
        label = f"  {_short_app_type(r['application_type'])}"
        count_fmt = f"{int(r['count']):,}"
        if prev_oh and r["application_type"] in prev_oh:
            change = count_change(prev_oh[r["application_type"]]["count"], r["count"])
            prev_fmt = f"{int(prev_oh[r['application_type']]['count']):,}"
            print(f"{label:<20}  {prev_fmt:>8}  →  {count_fmt:<8}  {change}")
        else:
            print(f"{label:<20}  {count_fmt}")

    # Applications received
    period = f"{curr_received[0]['period_start']} – {curr_received[0]['period_end']}" if curr_received else ""
    print(f"\nApplications Received ({period}):")
    prev_rec = {r["application_type"]: r for r in (prev_received or [])}
    for r in curr_received:
        label = f"  {_short_app_type(r['application_type'])}"
        count_fmt = f"{int(r['count']):,}"
        if prev_rec and r["application_type"] in prev_rec:
            change = count_change(prev_rec[r["application_type"]]["count"], r["count"])
            prev_fmt = f"{int(prev_rec[r['application_type']]['count']):,}"
            print(f"{label:<20}  {prev_fmt:>8}  →  {count_fmt:<8}  {change}")
        else:
            print(f"{label:<20}  {count_fmt}")

    print()


# ---------------------------------------------------------------------------
# LATEST.md (Option B)
# ---------------------------------------------------------------------------

def write_latest_md(
    prev_processing: list[dict] | None,
    curr_processing: list[dict],
    prev_on_hand: list[dict] | None,
    curr_on_hand: list[dict],
    prev_received: list[dict] | None,
    curr_received: list[dict],
    curr_date: str,
    prev_date: str,
    scrape_timestamp: str,
):
    prev_pt = {(r["application_type"], r["period_counted"]): r for r in (prev_processing or [])}
    prev_oh = {r["application_type"]: r for r in (prev_on_hand or [])}
    prev_rec = {r["application_type"]: r for r in (prev_received or [])}

    period = (
        f"{curr_received[0]['period_start']} – {curr_received[0]['period_end']}"
        if curr_received else "—"
    )
    prev_label = f"Previously: {prev_date}" if prev_date else "First snapshot"

    lines = [
        f"> **Report date:** {curr_date} &nbsp;|&nbsp; {prev_label} &nbsp;|&nbsp; **Scraped:** {scrape_timestamp}",
        "",
        f"Source: [Department of Home Affairs]({URL})",
        "",
        "---",
        "",
        "## Processing Times",
        "",
        "Time taken to process 90% of applications (lower is better).",
        "",
        "| Application type | Period | p25 | p50 | p75 | p90 | Change (p90) |",
        "|---|---|---|---|---|---|---|",
    ]

    for r in curr_processing:
        key = (r["application_type"], r["period_counted"])
        app = _short_app_type(r["application_type"])
        change_cell = "—"
        if prev_pt and key in prev_pt:
            old_p90 = prev_pt[key]["p90"]
            change_cell = f"{old_p90} → {r['p90']}  {duration_trend(old_p90, r['p90'])}"
        lines.append(
            f"| {app} | {r['period_counted']} | {r['p25']} | {r['p50']} | {r['p75']} | {r['p90']} | {change_cell} |"
        )

    lines += [
        "",
        "---",
        "",
        f"## Applications on Hand (as of {curr_date})",
        "",
        "| Application type | Count | Change |",
        "|---|---|---|",
    ]

    for r in curr_on_hand:
        app = _short_app_type(r["application_type"])
        count_fmt = f"{int(r['count']):,}"
        change_cell = "—"
        if prev_oh and r["application_type"] in prev_oh:
            change_cell = count_change(prev_oh[r["application_type"]]["count"], r["count"])
        lines.append(f"| {app} | {count_fmt} | {change_cell} |")

    lines += [
        "",
        "---",
        "",
        f"## Applications Received ({period})",
        "",
        "| Application type | Count | Change vs previous month |",
        "|---|---|---|",
    ]

    for r in curr_received:
        app = _short_app_type(r["application_type"])
        count_fmt = f"{int(r['count']):,}"
        change_cell = "—"
        if prev_rec and r["application_type"] in prev_rec:
            change_cell = count_change(prev_rec[r["application_type"]]["count"], r["count"])
        lines.append(f"| {app} | {count_fmt} | {change_cell} |")

    lines += [
        "",
        "---",
        "",
        "_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._",
    ]

    static_intro = [
        "# Citizenship Processing Times",
        "",
        f"This project scrapes the Australian Department of Home Affairs [citizenship processing times page]({URL}) daily, stores the data in CSV files, and automatically updates this README when the government publishes new monthly figures — showing processing time trends, backlog size, and application intake with month-over-month change indicators.",
        "",
        "## Run locally",
        "",
        "```bash",
        "uv run main.py",
        "```",
        "",
        "## Run tests",
        "",
        "```bash",
        "uv run pytest tests/ -v",
        "```",
        "",
        "---",
        "",
        "## Latest Data",
        "",
    ]

    README_MD.write_text("\n".join(static_intro + lines) + "\n", encoding="utf-8")
    print(f"  README.md written.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    scrape_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Scraping at {scrape_timestamp} ...")

    html = fetch_page_html()
    soup = BeautifulSoup(html, "html.parser")

    # Extract all three sections
    processing_rows = extract_processing_times(soup)
    report_date, on_hand_rows = extract_applications_on_hand(soup)
    _, _, received_rows = extract_applications_received(soup)

    # Load previous snapshots before appending new data
    prev_pt, curr_pt_saved = two_most_recent(
        load_snapshots_by_date(DATA_DIR / "processing_times.csv", "scrape_timestamp")
    )
    prev_oh_snap, _ = two_most_recent(
        load_snapshots_by_date(DATA_DIR / "applications_on_hand.csv", "report_date")
    )
    prev_rec_snap, _ = two_most_recent(
        load_snapshots_by_date(DATA_DIR / "applications_received.csv", "period_end")
    )

    # Detect whether this is new government data or a repeat scrape
    on_hand_snapshots = load_snapshots_by_date(DATA_DIR / "applications_on_hand.csv", "report_date")
    is_new_data = report_date not in on_hand_snapshots

    # Save to CSVs
    append_csv(
        DATA_DIR / "processing_times.csv",
        ["scrape_timestamp", "application_type", "period_counted", "p25", "p50", "p75", "p90"],
        [{"scrape_timestamp": scrape_timestamp, **r} for r in processing_rows],
    )
    append_csv(
        DATA_DIR / "applications_on_hand.csv",
        ["scrape_timestamp", "report_date", "application_type", "count"],
        [{"scrape_timestamp": scrape_timestamp, **r} for r in on_hand_rows],
    )
    append_csv(
        DATA_DIR / "applications_received.csv",
        ["scrape_timestamp", "period_start", "period_end", "application_type", "count"],
        [{"scrape_timestamp": scrape_timestamp, **r} for r in received_rows],
    )
    print(f"  Saved: {len(processing_rows)} processing rows, {len(on_hand_rows)} on-hand rows, {len(received_rows)} received rows.")

    if is_new_data:
        prev_date = list(on_hand_snapshots.keys())[-1] if on_hand_snapshots else ""

        print_change_summary(
            prev_processing=list(prev_oh_snap) if prev_oh_snap else None,  # fallback; see note below
            curr_processing=processing_rows,
            prev_on_hand=prev_oh_snap,
            curr_on_hand=on_hand_rows,
            prev_received=prev_rec_snap,
            curr_received=received_rows,
            prev_date=prev_date,
            curr_date=report_date,
        )

        write_latest_md(
            prev_processing=curr_pt_saved,
            curr_processing=processing_rows,
            prev_on_hand=prev_oh_snap,
            curr_on_hand=on_hand_rows,
            prev_received=prev_rec_snap,
            curr_received=received_rows,
            curr_date=report_date,
            prev_date=prev_date,
            scrape_timestamp=scrape_timestamp,
        )
    else:
        print(f"  No new data (report date unchanged: {report_date}). Skipping summary.")

    print("Done.")


if __name__ == "__main__":
    main()
