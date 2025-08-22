{{ config(materialized='table') }}

WITH yearly_total AS (
    SELECT
        DATE_TRUNC('year', sale_date)::date AS sale_year,
        ROUND(SUM(weekly_sales)::numeric, 2) AS yearly_total_sales
    FROM landing_sales
    GROUP BY sale_year
),

with_lag AS (
    SELECT
        sale_year,
        yearly_total_sales,
        LEAD(yearly_total_sales) OVER (ORDER BY sale_year) AS prev_year_sales
    FROM yearly_total
)

SELECT
    sale_year,
    yearly_total_sales,
    ROUND(
        100.0 * (yearly_total_sales - prev_year_sales) / NULLIF(prev_year_sales, 0),
        2
    ) AS yoy_growth_pct
FROM with_lag
ORDER BY sale_year
