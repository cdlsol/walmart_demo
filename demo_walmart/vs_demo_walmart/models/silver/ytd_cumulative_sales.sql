{{ config(materialized='view') }}
--YTD cumulative sales (per store, per month)
WITH monthly AS (
  SELECT
    store,
    DATE_TRUNC('month', sale_date) AS sale_month,
    SUM(weekly_sales) AS monthly_total_sales
  FROM landing_sales
  GROUP BY store, DATE_TRUNC('month', sale_date)
)
SELECT
  store,
  sale_month,
  monthly_total_sales,
  SUM(monthly_total_sales) OVER (
    PARTITION BY store, DATE_TRUNC('year', sale_month)
    ORDER BY sale_month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS ytd_sales
FROM monthly
ORDER BY store, sale_month
