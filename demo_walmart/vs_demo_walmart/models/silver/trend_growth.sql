{{ config(materialized='view') }}
--Trend and growth
WITH monthly AS (
  SELECT
    store,
    DATE_TRUNC('month', sale_date)::date AS sale_month,
    SUM(weekly_sales) AS monthly_total_sales
  FROM landing_sales
  GROUP BY store, DATE_TRUNC('month', sale_date)
)
SELECT
  store,
  sale_month,
  monthly_total_sales,
  ROUND( (100.0 * (monthly_total_sales - LAG(monthly_total_sales) OVER
          (PARTITION BY store ORDER BY sale_month))
        / NULLIF(LAG(monthly_total_sales) OVER
          (PARTITION BY store ORDER BY sale_month), 0))::numeric
      , 2) AS mom_growth_pct
FROM monthly
ORDER BY store, sale_month
