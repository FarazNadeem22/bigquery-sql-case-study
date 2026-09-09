# BigQuery SQL Case Study — Country-wise GDP growth momentum

## Business problem
Comparing GDP growth for Pakistan, India, China, Brazil and the USA. Showing which countries have shown the most GDP growth momentum over 2015-2020, and how they compare year over year.

## Approach
1. **Extract & explore (BigQuery)** — query `bigquery-public-data.world_bank_wdi.indicators_data` , filtered to indicator `NY.GDP.MKTP.KD.ZG`
2. **Transform (SQL + window functions)** — a chained CTE pipeline computing period-over-period GDP growth (`LAG` for prior year comparision), ranked within year (`RANK()`)
3. **Analyze (Python)** — pull the aggregated result into pandas via the BigQuery client, compute a summary metric, produce one chart.
4. **So what** — a written recommendation: which countries merit closer research attention and why, stated the way you'd brief a portfolio manager, not just "here's a chart."

## Why BigQuery / GCP
Chosen deliberately for its native SQL-at-scale workflow and market demand,  see the course's syllabus README for the full reasoning. Every query here is designed around BigQuery's scan-based cost model (filtered, partition-aware, `SELECT` only needed columns) rather than treated as generic SQL.

## Repo structure
```
queries/          -- standalone .sql files, one query per analytical step
scripts/          -- Python: pulls query results into pandas, produces charts
requirements.txt
```

## Status
Scaffolded from Week 1-2 of the refresher course (see `queries/01_gdp_growth_momentum.sql` and `scripts/analyze_momentum.py`). This is now a working small project.

## So what
*`China` came out on top for the most average GDP growth percent at `5.99%` followed by `India` at `4.39%` and then `Pakistan` at `3.64%` the `USA` and `Brazil` came in last at `1.48%` and `-1.06%`*

## Honest scope notes
- Uses public World Bank WDI only - no proprietary or paid data sources.
- Momentum score here is a simple, transparent rolling-growth ranking, not a proprietary factor model — the point is demonstrating clean SQL/analytical methodology, not claiming an edge.
