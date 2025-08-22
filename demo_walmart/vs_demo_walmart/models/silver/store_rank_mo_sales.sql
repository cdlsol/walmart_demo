{{ config(materialized='view') }}

WITH monthly AS (
  SELECT
    store,
    (DATE_TRUNC('month', sale_date))::date AS sale_month,  -- ← cast to date
    SUM(weekly_sales) AS monthly_sales
  FROM landing_sales
  GROUP BY store, (DATE_TRUNC('month', sale_date))::date
)
SELECT
  store,
  sale_month,
  monthly_sales,
  RANK() OVER (PARTITION BY sale_month ORDER BY monthly_sales DESC) AS sales_rank
FROM monthly
