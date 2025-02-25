{{
    config(
        materialized = 'table'
    )
}}
WITH agg_trips AS (
  SELECT 
    pickup_year
  , pickup_quarter
  , CONCAT(pickup_year, '_', pickup_quarter) AS year_quarter
  , service_type
  , SUM(total_amount) AS quarterly_revenue
  FROM {{ ref('fact_trips') }}
  WHERE 1=1
        AND pickup_year >= 2019 
        AND pickup_year < 2021
  GROUP BY 1,2,3,4
  -- LIMIT 100
)

, quarterly_yoy_revenue AS (
  SELECT 
    pickup_year
  , pickup_quarter
  , year_quarter
  , service_type
  , quarterly_revenue 
  , LAG(quarterly_revenue) OVER(PARTITION BY service_type, pickup_quarter ORDER BY pickup_year) AS last_quarterly_revenue
  , LAG(year_quarter) OVER(PARTITION BY service_type, pickup_quarter ORDER BY pickup_year) AS last_quarterly_revenue_year_quarter
  FROM agg_trips
)

SELECT *
FROM quarterly_yoy_revenue