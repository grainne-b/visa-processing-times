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

## Latest Data — 28 February 2026

> **Site last updated:**  &nbsp;|&nbsp; **Scraped:** 2026-03-24T05:23:32Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 9 months | ↓ faster (was 10 months) |
| Processing time — Approval → Ceremony | 6 months | → unchanged |
| Processing time — From date of application to ceremony | 14 months | ↓ faster (was 15 months) |
| Processing time — Application → Decision | 7 months | → unchanged |
| Processing time — Application → Decision | 16 days | ↑ slower (was 15 days) |
| Applications on hand (By conferral) | 79,770 | ↓ -11,434 (-12.5%) |
| Applications on hand (By descent) | 5,997 | ↓ -894 (-13.0%) |
| Applications on hand (Evidence) | 711 | ↓ -212 (-23.0%) |
| Applications received (1 February 2026 – 28 February 2026, By conferral) | 16,483 | ↓ -407 (-2.4%) |
| Applications received (1 February 2026 – 28 February 2026, By descent) | 1,868 | ↑ +112 (+6.4%) |
| Applications received (1 February 2026 – 28 February 2026, Evidence) | 3,600 | ↑ +88 (+2.5%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 9 months | 10 months → 9 months  ↓ faster |
| By conferral | Approval → Ceremony | 6 months | 6 months → 6 months  → unchanged |
| By conferral | From date of application to ceremony | 14 months | 15 months → 14 months  ↓ faster |
| By descent | Application → Decision | 7 months | 7 months → 7 months  → unchanged |
| Evidence | Application → Decision | 16 days | 15 days → 16 days  ↑ slower |

---

## Applications on Hand (as of 28 February 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 79,770 | ↓ -11,434 (-12.5%) |
| By descent | 5,997 | ↓ -894 (-13.0%) |
| Evidence | 711 | ↓ -212 (-23.0%) |

---

## Applications Received (1 February 2026 – 28 February 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 16,483 | ↓ -407 (-2.4%) |
| By descent | 1,868 | ↑ +112 (+6.4%) |
| Evidence | 3,600 | ↑ +88 (+2.5%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 28 February 2026 | 9 months | 6 months | 79,770 | 16,483 | 24,775 |
| 31 January 2026 | 10 months | 6 months | 88,062 | — | — |
| 31 December 2025 | 11 months | 6 months | 91,204 | 16,890 | — |

---

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
