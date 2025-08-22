{{ config(materialized='table') }}


WITH monthly_sales AS (
    SELECT
        store,
        DATE_TRUNC('month', sale_date) AS sale_month,
        ROUND(SUM(weekly_sales)::numeric, 2) AS monthly_total_sales
    FROM landing_sales
    GROUP BY store, DATE_TRUNC('month', sale_date)
),
with_lag AS (
    SELECT
        store,
        sale_month,
        monthly_total_sales,
        LAG(monthly_total_sales) OVER (PARTITION BY store ORDER BY sale_month) AS prev_month
    FROM monthly_sales
)
SELECT
    store,
    sale_month,
    monthly_total_sales,
    ROUND(
        (100.0 * (monthly_total_sales - prev_month) / NULLIF(prev_month, 0))::numeric, 2
    ) AS mom_growth_pct
FROM with_lag

