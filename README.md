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

## Latest Data — 30 September 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-10-16T08:46:22Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 5 months | → unchanged |
| Processing time — Approval → Ceremony | 6 months | → unchanged |
| Processing time — From date of application to ceremony | 11 months | ↓ faster (was 12 months) |
| Processing time — Application → Decision | 4 months | → unchanged |
| Processing time — Application → Decision | 15 days | ↓ faster (was 16 days) |
| Applications on hand (By conferral) | 53,298 | ↓ -2,986 (-5.3%) |
| Applications on hand (By descent) | 2,988 | ↓ -445 (-13.0%) |
| Applications on hand (Evidence) | 940 | ↑ +41 (+4.6%) |
| Applications received (1 September 2026 – 30 September 2026, By conferral) | 23,581 | ↓ -509 (-2.1%) |
| Applications received (1 September 2026 – 30 September 2026, By descent) | 1,664 | ↑ +83 (+5.2%) |
| Applications received (1 September 2026 – 30 September 2026, Evidence) | 3,647 | ↓ -488 (-11.8%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 5 months | 5 months → 5 months  → unchanged |
| By conferral | Approval → Ceremony | 6 months | 6 months → 6 months  → unchanged |
| By conferral | From date of application to ceremony | 11 months | 12 months → 11 months  ↓ faster |
| By descent | Application → Decision | 4 months | 4 months → 4 months  → unchanged |
| Evidence | Application → Decision | 15 days | 16 days → 15 days  ↓ faster |

---

## Applications on Hand (as of 30 September 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 53,298 | ↓ -2,986 (-5.3%) |
| By descent | 2,988 | ↓ -445 (-13.0%) |
| Evidence | 940 | ↑ +41 (+4.6%) |

---

## Applications Received (1 September 2026 – 30 September 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 23,581 | ↓ -509 (-2.1%) |
| By descent | 1,664 | ↑ +83 (+5.2%) |
| Evidence | 3,647 | ↓ -488 (-11.8%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 30 September 2026 | 5 months | 6 months | 53,298 | 23,581 | 25,498 |
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
