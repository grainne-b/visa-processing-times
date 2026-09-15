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

## Latest Data — 31 August 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-09-15T09:13:40Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 5 months | ↓ faster (was 6 months) |
| Processing time — Approval → Ceremony | 6 months | → unchanged |
| Processing time — From date of application to ceremony | 12 months | ↓ faster (was 13 months) |
| Processing time — Application → Decision | 4 months | ↓ faster (was 5 months) |
| Processing time — Application → Decision | 16 days | ↑ slower (was 12 days) |
| Applications on hand (By conferral) | 55,215 | ↓ -7,468 (-11.9%) |
| Applications on hand (By descent) | 3,358 | ↓ -540 (-13.9%) |
| Applications on hand (Evidence) | 855 | ↑ +233 (+37.5%) |
| Applications received (1 August 2026 – 31 August 2026, By conferral) | 24,422 | ↑ +3,356 (+15.9%) |
| Applications received (1 August 2026 – 31 August 2026, By descent) | 1,703 | ↑ +21 (+1.2%) |
| Applications received (1 August 2026 – 31 August 2026, Evidence) | 3,974 | ↑ +408 (+11.4%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 5 months | 6 months → 5 months  ↓ faster |
| By conferral | Approval → Ceremony | 6 months | 6 months → 6 months  → unchanged |
| By conferral | From date of application to ceremony | 12 months | 13 months → 12 months  ↓ faster |
| By descent | Application → Decision | 4 months | 5 months → 4 months  ↓ faster |
| Evidence | Application → Decision | 16 days | 12 days → 16 days  ↑ slower |

---

## Applications on Hand (as of 31 August 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 55,215 | ↓ -7,468 (-11.9%) |
| By descent | 3,358 | ↓ -540 (-13.9%) |
| Evidence | 855 | ↑ +233 (+37.5%) |

---

## Applications Received (1 August 2026 – 31 August 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 24,422 | ↑ +3,356 (+15.9%) |
| By descent | 1,703 | ↑ +21 (+1.2%) |
| Evidence | 3,974 | ↑ +408 (+11.4%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 31 August 2026 | 5 months | 6 months | 55,215 | 24,422 | 25,491 |
| 31 July 2026 | 6 months | 6 months | 56,284 | 24,090 | 30,489 |
| 30 June 2026 | 6 months | 7 months | 62,683 | — | — |
| 31 May 2026 | 7 months | 6 months | 62,084 | — | — |
| 30 April 2026 | 8 months | 6 months | 70,151 | 17,175 | 21,316 |
| 31 March 2026 | 8 months | 6 months | 74,292 | 17,898 | 23,376 |
| 28 February 2026 | 9 months | 6 months | 79,770 | 16,483 | 24,775 |
| 31 January 2026 | 10 months | 6 months | 88,062 | — | — |
| 31 December 2025 | 11 months | 6 months | 91,204 | 16,890 | — |

---

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
