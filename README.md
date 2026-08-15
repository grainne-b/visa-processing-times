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

## Latest Data — 31 July 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-08-15T04:29:55Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 6 months | → unchanged |
| Processing time — Approval → Ceremony | 6 months | ↓ faster (was 7 months) |
| Processing time — From date of application to ceremony | 13 months | ↓ faster (was 14 months) |
| Processing time — Application → Decision | 5 months | → unchanged |
| Processing time — Application → Decision | 12 days | ↓ faster (was 16 days) |
| Applications on hand (By conferral) | 56,284 | ↓ -5,800 (-9.3%) |
| Applications on hand (By descent) | 3,433 | ↓ -997 (-22.5%) |
| Applications on hand (Evidence) | 899 | ↑ +78 (+9.5%) |
| Applications received (1 July 2026 – 31 July 2026, By conferral) | 24,090 | ↑ +4,742 (+24.5%) |
| Applications received (1 July 2026 – 31 July 2026, By descent) | 1,581 | ↓ -24 (-1.5%) |
| Applications received (1 July 2026 – 31 July 2026, Evidence) | 4,135 | ↑ +522 (+14.4%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 6 months | 6 months → 6 months  → unchanged |
| By conferral | Approval → Ceremony | 6 months | 7 months → 6 months  ↓ faster |
| By conferral | From date of application to ceremony | 13 months | 14 months → 13 months  ↓ faster |
| By descent | Application → Decision | 5 months | 5 months → 5 months  → unchanged |
| Evidence | Application → Decision | 12 days | 16 days → 12 days  ↓ faster |

---

## Applications on Hand (as of 31 July 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 56,284 | ↓ -5,800 (-9.3%) |
| By descent | 3,433 | ↓ -997 (-22.5%) |
| Evidence | 899 | ↑ +78 (+9.5%) |

---

## Applications Received (1 July 2026 – 31 July 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 24,090 | ↑ +4,742 (+24.5%) |
| By descent | 1,581 | ↓ -24 (-1.5%) |
| Evidence | 4,135 | ↑ +522 (+14.4%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
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
