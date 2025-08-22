{{ config(materialized='view') }}


--Rolling 3-month average (per store, per month)
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
  ROUND(AVG(monthly_total_sales) OVER
        (PARTITION BY store ORDER BY sale_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)::numeric, 2)
    AS rolling_3m_avg
FROM monthly
ORDER BY store, sale_month
