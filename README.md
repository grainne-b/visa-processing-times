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

## Latest Data

> **Report date:** 31 January 2026 &nbsp;|&nbsp; Previously: 31 December 2025 &nbsp;|&nbsp; **Scraped:** 2026-03-16T04:15:00Z

Source: [Department of Home Affairs](https://immi.homeaffairs.gov.au/citizenship/citizenship-processing-times/citizenship-processing-times)

---

## Processing Times

Time taken to process 90% of applications (lower is better).

| Application type | Period | p25 | p50 | p75 | p90 | Change (p90) |
|---|---|---|---|---|---|---|
| By conferral | From date of application to decision 2 | 5 months | 6 months | 8 months | 10 months | 11 months → 10 months  ↓ faster |
| By conferral | From date of approval to ceremony | 4 months | 5 months | 5 months | 6 months | 6 months → 6 months  → unchanged |

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

_Data is published monthly by the Department of Home Affairs. This file is auto-updated when new data is detected._
