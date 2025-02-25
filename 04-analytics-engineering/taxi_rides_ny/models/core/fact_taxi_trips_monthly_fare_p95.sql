{{
    config(
        materialized = 'table'
    )
}}

WITH trip_fare_percentiles AS (
  SELECT 
    pickup_year
  , pickup_month
  , service_type
  , fare_amount
  , PERCENTILE_CONT(fare_amount, 0.5) OVER(PARTITION BY pickup_year, pickup_month, service_type) AS p50
  , PERCENTILE_CONT(fare_amount, 0.9) OVER(PARTITION BY pickup_year, pickup_month, service_type) AS p90
  , PERCENTILE_CONT(fare_amount, 0.95) OVER(PARTITION BY pickup_year, pickup_month, service_type) AS p95
  , PERCENTILE_CONT(fare_amount, 0.97) OVER(PARTITION BY pickup_year, pickup_month, service_type) AS p97
  FROM {{ ref('fact_trips') }}
  WHERE 1=1
        AND pickup_year >= 2019 
        AND pickup_year < 2021
        AND fare_amount > 0 
        AND trip_distance > 0
        AND LOWER(payment_type_description) IN ('cash', 'credit card')
)

SELECT 
  pickup_year
, pickup_month
, service_type
, MIN(fare_amount) AS min_fare_amount
, AVG(fare_amount) AS avg_fare_amount
, ANY_VALUE(p50) AS p50
, ANY_VALUE(p90) AS p90
, ANY_VALUE(p95) AS p95
, ANY_VALUE(p97) AS p97
, MAX(fare_amount) AS max_fare_amount
FROM trip_fare_percentiles
GROUP BY 1,2,3