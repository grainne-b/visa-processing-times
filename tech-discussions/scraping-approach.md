# Scraping Approach: Citizenship Processing Times

## Page
https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times

## Data to Scrape
- Processing times
- Number of applications we have
- Number of applications received

## Technical Findings

### Page Type
The page is **SharePoint-based and JavaScript-rendered**. The raw HTML contains only a page shell — the actual data tables are injected after JavaScript executes. A plain `requests` fetch confirmed this: the heading was present but no data.

### Scraping Options Considered

| Approach | Works for this page? | Complexity | Decision |
|----------|---------------------|------------|----------|
| `requests` + `BeautifulSoup` | No (JS-rendered) | Low | Ruled out |
| Hidden API endpoint (if exists) | Possibly yes | Low | Investigate first |
| `playwright` headless browser | Yes, guaranteed | Medium | Fallback if no API found |

## Decision

**Playwright with headless Chromium** is required. Investigation confirmed:
- The page is SharePoint-based and data is fully JS-rendered — `requests` returns no data
- The site actively blocks headless browsers (returns "Access Denied" without evasion)
- **`playwright-stealth`** is used to bypass headless detection, enabling the scraper to run in CI without a display

The Playwright MCP server was used during development to inspect the page structure and confirm data availability.

## Language, Tooling & Output
- **Language:** Python 3.13 (latest stable with broad ecosystem support; 3.14 available but too new for library compatibility)
- **Package manager:** `uv` — fast, modern Python package/project manager
- **Output:** CSV file (appended on each run, with timestamp per row)
- **Scheduling:** GitHub Actions (daily) — to be added later

## Output CSV Files
Three files in `data/`, each appended on every run:

| File | Columns |
|------|---------|
| `processing_times.csv` | `scrape_timestamp, application_type, period_counted, p25, p50, p75, p90` |
| `applications_on_hand.csv` | `scrape_timestamp, report_date, application_type, count` |
| `applications_received.csv` | `scrape_timestamp, period_start, period_end, application_type, count` |

## Change Detection & Display

The government updates the page **monthly**, not daily. Most daily scrapes will return the same data. The script handles this by:

1. Comparing the scraped `report_date` against the last saved date in `applications_on_hand.csv`
2. If new data is detected:
   - **Console output (Option A):** prints a formatted diff to stdout (visible in GitHub Actions logs)
   - **README.md (Option B):** rewrites `README.md` with a static project intro + the latest data tables including change indicators (↑ ↓ →)
3. If no new data: prints "No new data — skipping summary"

### Trend indicators
- Processing times: `↓ faster` / `↑ slower` / `→ unchanged` (duration compared via approximate days: 1 month = 30 days)
- Counts: `↑ +N (+X%)` / `↓ -N (-X%)` / `→` with percentage change

## Next Steps
1. ~~Implement scraper~~ (done)
2. ~~Implement change detection + console + README output~~ (done)
3. Add GitHub Actions workflow for daily scheduling
