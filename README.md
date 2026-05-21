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

## Latest Data — 30 April 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-05-21T07:53:07Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 8 months | → unchanged |
| Processing time — Approval → Ceremony | 6 months | → unchanged |
| Processing time — From date of application to ceremony | 14 months | → unchanged |
| Processing time — Application → Decision | 6 months | → unchanged |
| Processing time — Application → Decision | 11 days | ↓ faster (was 12 days) |
| Applications on hand (By conferral) | 70,151 | ↓ -9,619 (-12.1%) |
| Applications on hand (By descent) | 5,492 | ↓ -505 (-8.4%) |
| Applications on hand (Evidence) | 756 | ↑ +45 (+6.3%) |
| Applications received (1 April 2026 – 30 April 2026, By conferral) | 17,175 | ↑ +692 (+4.2%) |
| Applications received (1 April 2026 – 30 April 2026, By descent) | 1,767 | ↓ -101 (-5.4%) |
| Applications received (1 April 2026 – 30 April 2026, Evidence) | 3,290 | ↓ -310 (-8.6%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 8 months | 8 months → 8 months  → unchanged |
| By conferral | Approval → Ceremony | 6 months | 6 months → 6 months  → unchanged |
| By conferral | From date of application to ceremony | 14 months | 14 months → 14 months  → unchanged |
| By descent | Application → Decision | 6 months | 6 months → 6 months  → unchanged |
| Evidence | Application → Decision | 11 days | 12 days → 11 days  ↓ faster |

---

## Applications on Hand (as of 30 April 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 70,151 | ↓ -9,619 (-12.1%) |
| By descent | 5,492 | ↓ -505 (-8.4%) |
| Evidence | 756 | ↑ +45 (+6.3%) |

---

## Applications Received (1 April 2026 – 30 April 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 17,175 | ↑ +692 (+4.2%) |
| By descent | 1,767 | ↓ -101 (-5.4%) |
| Evidence | 3,290 | ↓ -310 (-8.6%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 30 April 2026 | 8 months | 6 months | 70,151 | 17,175 | 21,316 |
| 31 March 2026 | 8 months | 6 months | 74,292 | 17,898 | 23,376 |
| 28 February 2026 | 9 months | 6 months | 79,770 | 16,483 | 24,775 |
| 31 January 2026 | 10 months | 6 months | 88,062 | — | — |
| 31 December 2025 | 11 months | 6 months | 91,204 | 16,890 | — |

---

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
