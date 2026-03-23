"""
Unit tests for main.py parsing functions.

All tests use the mock HTML fixture at tests/fixtures/mock_page.html, which
mirrors the DOM structure of the real page after JavaScript has rendered it.
No network calls or browser instances are used in these tests.
"""

import csv
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from main import (
    append_csv,
    count_change,
    duration_trend,
    extract_applications_on_hand,
    extract_applications_received,
    extract_last_updated,
    extract_processing_times,
    find_section_table,
    load_snapshots_by_date,
    parse_duration_days,
    parse_table,
    two_most_recent,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "mock_page.html"


@pytest.fixture
def soup():
    return BeautifulSoup(FIXTURE_PATH.read_text(encoding="utf-8"), "html.parser")


# ---------------------------------------------------------------------------
# parse_table
# ---------------------------------------------------------------------------

class TestParseTable:
    def test_returns_header_and_data_rows(self, soup):
        table = soup.find("table")
        rows = parse_table(table)
        # Header row + 5 data rows for processing times
        assert len(rows) == 6

    def test_header_row_content(self, soup):
        table = soup.find("table")
        rows = parse_table(table)
        assert rows[0][0] == "Application type"
        assert rows[0][1] == "Period counted"

    def test_strips_whitespace_from_cells(self, soup):
        table = soup.find("table")
        rows = parse_table(table)
        for row in rows:
            for cell in row:
                assert cell == cell.strip()

    def test_superscripts_included_in_text(self, soup):
        """Footnote numbers (e.g. superscript '1') are part of the cell text."""
        table = soup.find("table")
        rows = parse_table(table)
        # The first data cell contains "... other situations) 1" (superscript becomes "1")
        assert "1" in rows[1][0]

    def test_merged_cell_row_has_five_cells(self, soup):
        """
        The 'by conferral' rowspan means sub-rows only produce 5 cells.
        Row index 2 = "From date of approval to ceremony" sub-row.
        """
        table = soup.find("table")
        rows = parse_table(table)
        assert len(rows[2]) == 5
        assert rows[2][0] == "From date of approval to ceremony"


# ---------------------------------------------------------------------------
# find_section_table
# ---------------------------------------------------------------------------

class TestFindSectionTable:
    def test_finds_processing_times_section(self, soup):
        paragraph, table = find_section_table(soup, "Processing times")
        assert table is not None

    def test_finds_on_hand_section(self, soup):
        paragraph, table = find_section_table(soup, "Number of applications we have")
        assert table is not None
        assert paragraph is not None

    def test_finds_received_section(self, soup):
        paragraph, table = find_section_table(soup, "Number of applications received")
        assert table is not None
        assert paragraph is not None

    def test_returns_none_for_missing_heading(self, soup):
        paragraph, table = find_section_table(soup, "This heading does not exist")
        assert paragraph is None
        assert table is None

    def test_heading_match_is_case_insensitive(self, soup):
        paragraph, table = find_section_table(soup, "processing times")
        assert table is not None

    def test_on_hand_paragraph_contains_date(self, soup):
        paragraph, _ = find_section_table(soup, "Number of applications we have")
        assert "31 January 2026" in paragraph.get_text()

    def test_received_paragraph_contains_period(self, soup):
        paragraph, _ = find_section_table(soup, "Number of applications received")
        assert "1 January" in paragraph.get_text()
        assert "31 January 2026" in paragraph.get_text()


# ---------------------------------------------------------------------------
# extract_processing_times
# ---------------------------------------------------------------------------

class TestExtractProcessingTimes:
    def test_returns_five_records(self, soup):
        records = extract_processing_times(soup)
        assert len(records) == 5

    def test_record_keys(self, soup):
        records = extract_processing_times(soup)
        expected_keys = {"application_type", "period_counted", "p25", "p50", "p75", "p90"}
        assert set(records[0].keys()) == expected_keys

    def test_first_record_values(self, soup):
        records = extract_processing_times(soup)
        first = records[0]
        assert "by conferral" in first["application_type"].lower()
        assert "application to decision" in first["period_counted"].lower()
        assert first["p25"] == "5 months"
        assert first["p90"] == "10 months"

    def test_merged_cell_rows_inherit_application_type(self, soup):
        """
        Rows 2 and 3 belong to 'by conferral' but their first cell is merged.
        The scraper must carry the application type forward from row 1.
        """
        records = extract_processing_times(soup)
        assert "by conferral" in records[1]["application_type"].lower()
        assert "by conferral" in records[2]["application_type"].lower()

    def test_merged_cell_rows_have_correct_period(self, soup):
        records = extract_processing_times(soup)
        assert records[1]["period_counted"] == "From date of approval to ceremony"
        assert records[2]["period_counted"] == "From date of application to ceremony"

    def test_by_descent_record(self, soup):
        records = extract_processing_times(soup)
        descent = records[3]
        assert "by descent" in descent["application_type"].lower()
        assert descent["p90"] == "7 months"

    def test_evidence_record(self, soup):
        records = extract_processing_times(soup)
        evidence = records[4]
        assert "evidence" in evidence["application_type"].lower()
        assert evidence["p25"] == "2 days"
        assert evidence["p90"] == "15 days"

    def test_returns_empty_list_when_heading_missing(self):
        soup = BeautifulSoup("<html><body><h2>Other heading</h2></body></html>", "html.parser")
        assert extract_processing_times(soup) == []


# ---------------------------------------------------------------------------
# extract_applications_on_hand
# ---------------------------------------------------------------------------

class TestExtractApplicationsOnHand:
    def test_returns_three_records(self, soup):
        _, records = extract_applications_on_hand(soup)
        assert len(records) == 3

    def test_record_keys(self, soup):
        _, records = extract_applications_on_hand(soup)
        assert set(records[0].keys()) == {"report_date", "application_type", "count"}

    def test_report_date_parsed(self, soup):
        report_date, _ = extract_applications_on_hand(soup)
        assert report_date == "31 January 2026"

    def test_report_date_on_each_record(self, soup):
        _, records = extract_applications_on_hand(soup)
        for record in records:
            assert record["report_date"] == "31 January 2026"

    def test_counts_are_numeric_strings_without_commas(self, soup):
        """Commas are stripped so counts can be cast to int downstream."""
        _, records = extract_applications_on_hand(soup)
        counts = [r["count"] for r in records]
        assert counts == ["88062", "6220", "865"]

    def test_conferral_record(self, soup):
        _, records = extract_applications_on_hand(soup)
        assert "by conferral" in records[0]["application_type"].lower()
        assert records[0]["count"] == "88062"

    def test_returns_empty_list_when_heading_missing(self):
        soup = BeautifulSoup("<html><body><h2>Other heading</h2></body></html>", "html.parser")
        _, records = extract_applications_on_hand(soup)
        assert records == []


# ---------------------------------------------------------------------------
# extract_applications_received
# ---------------------------------------------------------------------------

class TestExtractApplicationsReceived:
    def test_returns_three_records(self, soup):
        _, _, records = extract_applications_received(soup)
        assert len(records) == 3

    def test_record_keys(self, soup):
        _, _, records = extract_applications_received(soup)
        assert set(records[0].keys()) == {"period_start", "period_end", "application_type", "count"}

    def test_period_parsed(self, soup):
        period_start, period_end, _ = extract_applications_received(soup)
        assert period_start == "1 January 2026"
        assert period_end == "31 January 2026"

    def test_period_on_each_record(self, soup):
        _, _, records = extract_applications_received(soup)
        for record in records:
            assert record["period_start"] == "1 January 2026"
            assert record["period_end"] == "31 January 2026"

    def test_counts_are_numeric_strings_without_commas(self, soup):
        _, _, records = extract_applications_received(soup)
        counts = [r["count"] for r in records]
        assert counts == ["17562", "1882", "3706"]

    def test_conferral_record(self, soup):
        _, _, records = extract_applications_received(soup)
        assert "by conferral" in records[0]["application_type"].lower()
        assert records[0]["count"] == "17562"

    def test_returns_empty_list_when_heading_missing(self):
        soup = BeautifulSoup("<html><body><h2>Other heading</h2></body></html>", "html.parser")
        _, _, records = extract_applications_received(soup)
        assert records == []


# ---------------------------------------------------------------------------
# append_csv
# ---------------------------------------------------------------------------

class TestAppendCsv:
    def test_creates_file_with_header_on_first_write(self, tmp_path):
        filepath = tmp_path / "test.csv"
        rows = [{"name": "Alice", "score": "10"}]
        append_csv(filepath, ["name", "score"], rows)

        lines = filepath.read_text().splitlines()
        assert lines[0] == "name,score"
        assert lines[1] == "Alice,10"

    def test_appends_without_duplicate_header(self, tmp_path):
        filepath = tmp_path / "test.csv"
        append_csv(filepath, ["name", "score"], [{"name": "Alice", "score": "10"}])
        append_csv(filepath, ["name", "score"], [{"name": "Bob", "score": "20"}])

        lines = filepath.read_text().splitlines()
        assert lines.count("name,score") == 1  # header appears exactly once
        assert len(lines) == 3  # header + 2 data rows

    def test_creates_parent_directories(self, tmp_path):
        filepath = tmp_path / "nested" / "dir" / "test.csv"
        append_csv(filepath, ["col"], [{"col": "value"}])
        assert filepath.exists()

    def test_written_values_are_readable_by_csv_reader(self, tmp_path):
        filepath = tmp_path / "test.csv"
        rows = [
            {"ts": "2026-01-01T00:00:00Z", "count": "42"},
            {"ts": "2026-01-02T00:00:00Z", "count": "99"},
        ]
        append_csv(filepath, ["ts", "count"], rows)

        with open(filepath, newline="") as f:
            reader = list(csv.DictReader(f))

        assert len(reader) == 2
        assert reader[0]["ts"] == "2026-01-01T00:00:00Z"
        assert reader[1]["count"] == "99"


# ---------------------------------------------------------------------------
# parse_duration_days
# ---------------------------------------------------------------------------

class TestParseDurationDays:
    def test_parses_months(self):
        assert parse_duration_days("5 months") == 150

    def test_parses_days(self):
        assert parse_duration_days("15 days") == 15

    def test_parses_single_month(self):
        assert parse_duration_days("1 month") == 30

    def test_returns_none_for_unrecognised_format(self):
        assert parse_duration_days("unknown") is None

    def test_case_insensitive(self):
        assert parse_duration_days("3 Months") == 90


# ---------------------------------------------------------------------------
# duration_trend
# ---------------------------------------------------------------------------

class TestDurationTrend:
    def test_improvement(self):
        assert duration_trend("11 months", "10 months") == "↓ faster"

    def test_worsening(self):
        assert duration_trend("10 months", "11 months") == "↑ slower"

    def test_unchanged_same_string(self):
        assert duration_trend("6 months", "6 months") == "→ unchanged"

    def test_unchanged_same_duration(self):
        assert duration_trend("15 days", "15 days") == "→ unchanged"

    def test_months_vs_days_improvement(self):
        # 1 month (30 days) vs 15 days — faster
        assert duration_trend("1 month", "15 days") == "↓ faster"


# ---------------------------------------------------------------------------
# count_change
# ---------------------------------------------------------------------------

class TestCountChange:
    def test_decrease(self):
        result = count_change("91204", "88062")
        assert "↓" in result
        assert "-3,142" in result
        assert "-3.4%" in result

    def test_increase(self):
        result = count_change("16890", "17562")
        assert "↑" in result
        assert "+672" in result
        assert "+4.0%" in result

    def test_no_change(self):
        result = count_change("1000", "1000")
        assert "→" in result

    def test_zero_old_returns_dash(self):
        assert count_change("0", "100") == "—"

    def test_invalid_value_returns_dash(self):
        assert count_change("n/a", "100") == "—"


# ---------------------------------------------------------------------------
# load_snapshots_by_date and two_most_recent
# ---------------------------------------------------------------------------

class TestLoadSnapshotsAndTwoMostRecent:
    def test_load_groups_by_date(self, tmp_path):
        filepath = tmp_path / "test.csv"
        append_csv(filepath, ["report_date", "application_type", "count"], [
            {"report_date": "31 December 2025", "application_type": "By conferral", "count": "91204"},
            {"report_date": "31 December 2025", "application_type": "By descent", "count": "6891"},
            {"report_date": "31 January 2026", "application_type": "By conferral", "count": "88062"},
        ])
        snapshots = load_snapshots_by_date(filepath, "report_date")
        assert set(snapshots.keys()) == {"31 December 2025", "31 January 2026"}
        assert len(snapshots["31 December 2025"]) == 2

    def test_load_returns_empty_dict_for_missing_file(self, tmp_path):
        assert load_snapshots_by_date(tmp_path / "missing.csv", "report_date") == {}

    def test_two_most_recent_returns_previous_and_current(self, tmp_path):
        filepath = tmp_path / "test.csv"
        append_csv(filepath, ["report_date", "count"], [
            {"report_date": "31 December 2025", "count": "91204"},
            {"report_date": "31 January 2026", "count": "88062"},
        ])
        snapshots = load_snapshots_by_date(filepath, "report_date")
        previous, current = two_most_recent(snapshots)
        assert current[0]["report_date"] == "31 January 2026"
        assert previous[0]["report_date"] == "31 December 2025"

    def test_two_most_recent_returns_none_previous_when_only_one_date(self, tmp_path):
        filepath = tmp_path / "test.csv"
        append_csv(filepath, ["report_date", "count"], [
            {"report_date": "31 January 2026", "count": "88062"},
        ])
        snapshots = load_snapshots_by_date(filepath, "report_date")
        previous, current = two_most_recent(snapshots)
        assert previous is None
        assert current[0]["report_date"] == "31 January 2026"

    def test_two_most_recent_returns_none_none_for_empty(self):
        previous, current = two_most_recent({})
        assert previous is None
        assert current is None


# ---------------------------------------------------------------------------
# extract_last_updated
# ---------------------------------------------------------------------------

class TestExtractLastUpdated:
    def test_found(self, soup):
        assert extract_last_updated(soup) == "24 February 2026"

    def test_not_found(self):
        assert extract_last_updated(BeautifulSoup("<html></html>", "html.parser")) == ""

    def test_case_insensitive(self):
        html = "<html><body><p>LAST UPDATED: 1 March 2026</p></body></html>"
        assert extract_last_updated(BeautifulSoup(html, "html.parser")) == "1 March 2026"
