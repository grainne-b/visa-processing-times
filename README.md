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

## Latest Data — 31 January 2026

> **Site last updated:** 4 March 2026 &nbsp;|&nbsp; **Scraped:** 2026-03-22T05:19:24Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

### At a Glance

| Metric | Current | Change vs previous month |
|---|---|---|
| Processing time — Application → Decision | 10 months | ↓ faster (was 11 months) |
| Processing time — Approval → Ceremony | 6 months | → unchanged |
| Applications on hand (By conferral) | 88,062 | ↓ -3,142 (-3.4%) |
| Applications received (1 January 2026 – 31 January 2026, By conferral) | 17,562 | ↑ +672 (+4.0%) |

---

## Processing Times

_Time by which 90% of applications are decided — lower is better._

| Application type | Period | p90 | Change |
|---|---|---|---|
| By conferral | Application → Decision | 10 months | 11 months → 10 months  ↓ faster |
| By conferral | Approval → Ceremony | 6 months | 6 months → 6 months  → unchanged |

---

## Applications on Hand (as of 31 January 2026)

| Application type | Count | Change |
|---|---|---|
| By conferral | 88,062 | ↓ -3,142 (-3.4%) |

---

## Applications Received (1 January 2026 – 31 January 2026)

| Application type | Count | Change vs previous month |
|---|---|---|
| By conferral | 17,562 | ↑ +672 (+4.0%) |

---

## Historical Data (By conferral)

_Est. processed = previous month on hand + received − current month on hand._

| Report date | App → Decision (p90) | Approval → Ceremony (p90) | On hand | Received | Est. processed |
|---|---|---|---|---|---|
| 31 January 2026 | 10 months | 6 months | 88,062 | 17,562 | 20,704 |
| 31 December 2025 | 11 months | 6 months | 91,204 | 16,890 | — |

---

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
