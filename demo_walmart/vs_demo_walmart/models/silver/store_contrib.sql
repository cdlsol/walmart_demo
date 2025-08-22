{{ config(materialized='view') }}

--Store contribution % of company total (per month)
WITH monthly AS (
  SELECT
    store,
    DATE_TRUNC('month', sale_date) AS sale_month,
    SUM(weekly_sales) AS monthly_sales
  FROM landing_sales
  GROUP BY store, DATE_TRUNC('month', sale_date)
)
SELECT
  store,
  sale_month,
  monthly_sales,
  ROUND( (100.0 * monthly_sales
          / NULLIF(SUM(monthly_sales) OVER (PARTITION BY sale_month), 0))::numeric
      , 2) AS contribution_pct
FROM monthly
ORDER BY sale_month, store
