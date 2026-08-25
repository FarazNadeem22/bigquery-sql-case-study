-- Revenue momentum by company/sector, ranked within sector per period.
-- Replace `your-project.your_dataset.financials` with your actual BigQuery source
-- (e.g., a table built from bigquery-public-data.sec_quarterly_financials).
--
-- Cost note: always check the BigQuery console's bytes-scanned estimate before
-- running on a large source table. Filter on partition columns (e.g., fiscal
-- quarter/date) wherever the source table is partitioned.

WITH raw_financials AS (
  SELECT
    company_name,
    sector,
    fiscal_quarter,
    revenue
  FROM `your-project.your_dataset.financials`
  WHERE fiscal_quarter >= '2024-Q1'   -- prune partitions if the table is partitioned
),

revenue_growth AS (
  SELECT
    company_name,
    sector,
    fiscal_quarter,
    revenue,
    LAG(revenue) OVER (
      PARTITION BY company_name ORDER BY fiscal_quarter
    ) AS prior_quarter_revenue,
    SAFE_DIVIDE(
      revenue - LAG(revenue) OVER (PARTITION BY company_name ORDER BY fiscal_quarter),
      LAG(revenue) OVER (PARTITION BY company_name ORDER BY fiscal_quarter)
    ) AS qoq_growth
  FROM raw_financials
),

sector_ranked AS (
  SELECT
    company_name,
    sector,
    fiscal_quarter,
    qoq_growth,
    RANK() OVER (
      PARTITION BY sector, fiscal_quarter ORDER BY qoq_growth DESC
    ) AS momentum_rank_in_sector
  FROM revenue_growth
  WHERE qoq_growth IS NOT NULL
)

SELECT *
FROM sector_ranked
ORDER BY sector, fiscal_quarter, momentum_rank_in_sector
LIMIT 1000;
