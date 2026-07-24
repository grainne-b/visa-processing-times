# Citizenship Processing Times

This project scrapes the Australian Department of Home Affairs [citizenship processing times page](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times) daily, stores the data in CSV files, and automatically updates this README when the government publishes new monthly figures — showing processing time trends, backlog size, and application intake with month-over-month change indicators.

## Run locally

```bash
uv run main.py
```

## Run tests

```bash
uv run pytest tests/ -v
```

---

## Latest Data — 30 June 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-07-24T06:25:47Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 6 months | ↓ faster (was 7 months) |
| Processing time — Approval → Ceremony | 7 months | ↑ slower (was 6 months) |
| Processing time — From date of application to ceremony | 14 months | → unchanged |
| Processing time — Application → Decision | 5 months | → unchanged |
| Processing time — Application → Decision | 16 days | ↑ slower (was 15 days) |
| Applications on hand (By conferral) | 62,683 | ↓ -7,468 (-10.6%) |
| Applications on hand (By descent) | 3,898 | ↓ -1,594 (-29.0%) |
| Applications on hand (Evidence) | 622 | ↓ -134 (-17.7%) |
| Applications received (1 June 2026 – 30 June 2026, By conferral) | 21,066 | ↑ +3,891 (+22.7%) |
| Applications received (1 June 2026 – 30 June 2026, By descent) | 1,682 | ↓ -85 (-4.8%) |
| Applications received (1 June 2026 – 30 June 2026, Evidence) | 3,566 | ↑ +276 (+8.4%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 6 months | 7 months → 6 months  ↓ faster |
| By conferral | Approval → Ceremony | 7 months | 6 months → 7 months  ↑ slower |
| By conferral | From date of application to ceremony | 14 months | 14 months → 14 months  → unchanged |
| By descent | Application → Decision | 5 months | 5 months → 5 months  → unchanged |
| Evidence | Application → Decision | 16 days | 15 days → 16 days  ↑ slower |

---

## Applications on Hand (as of 30 June 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 62,683 | ↓ -7,468 (-10.6%) |
| By descent | 3,898 | ↓ -1,594 (-29.0%) |
| Evidence | 622 | ↓ -134 (-17.7%) |

---

## Applications Received (1 June 2026 – 30 June 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 21,066 | ↑ +3,891 (+22.7%) |
| By descent | 1,682 | ↓ -85 (-4.8%) |
| Evidence | 3,566 | ↑ +276 (+8.4%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 30 June 2026 | 6 months | 7 months | 62,683 | — | — |
| 31 May 2026 | 7 months | 6 months | 62,084 | — | — |
| 30 April 2026 | 8 months | 6 months | 70,151 | 17,175 | 21,316 |
| 31 March 2026 | 8 months | 6 months | 74,292 | 17,898 | 23,376 |
| 28 February 2026 | 9 months | 6 months | 79,770 | 16,483 | 24,775 |
| 31 January 2026 | 10 months | 6 months | 88,062 | — | — |
| 31 December 2025 | 11 months | 6 months | 91,204 | 16,890 | — |

---

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
