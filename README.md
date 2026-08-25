# BigQuery SQL Case Study — Sector Financial Momentum

## Business problem
Which sectors have shown the strongest and most consistent revenue growth momentum over recent reporting periods, and how does that momentum compare to price-based sentiment for the same names? A portfolio or research team asks this kind of question when deciding where to allocate research attention — this repo answers it end to end, from raw public data to a stated recommendation.

## Approach
1. **Extract & explore (BigQuery)** — query `bigquery-public-data.sec_quarterly_financials` (or a comparable public financial dataset) for revenue trends by sector/company, using a partition-aware, cost-conscious query design.
2. **Transform (SQL + window functions)** — a chained CTE pipeline computing period-over-period revenue growth (`LAG`) and a rolling momentum score, ranked within sector (`RANK()`/`DENSE_RANK()`).
3. **Analyze (Python)** — pull the aggregated result into pandas via the BigQuery client, compute a summary metric, produce one chart.
4. **So what** — a written recommendation: which sector(s) merit closer research attention and why, stated the way you'd brief a portfolio manager, not just "here's a chart."

## Why BigQuery / GCP
Chosen deliberately for its native SQL-at-scale workflow and market demand — see the course's syllabus README for the full reasoning. Every query here is designed around BigQuery's scan-based cost model (filtered, partition-aware, `SELECT` only needed columns) rather than treated as generic SQL.

## Repo structure
```
queries/          -- standalone .sql files, one query per analytical step
scripts/          -- Python: pulls query results into pandas, produces charts
requirements.txt
```

## Status
Scaffolded from Week 1-2 of the refresher course (see `queries/01_revenue_momentum.sql` and `scripts/analyze_momentum.py`). Replace the placeholder dataset/table references with your actual GCP project once your BigQuery sandbox is set up, run the pipeline, and fill in the "So what" section below with your actual finding.

## So what
*(Fill in after running the analysis: which sector, what magnitude of momentum, what you'd recommend a research team look at next.)*

## Honest scope notes
- Uses public SEC/financial datasets only — no proprietary or paid data sources.
- Momentum score here is a simple, transparent rolling-growth ranking, not a proprietary factor model — the point is demonstrating clean SQL/analytical methodology, not claiming an edge.
