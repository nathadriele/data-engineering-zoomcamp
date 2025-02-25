{{
    config(
        materialized='table'
    )
}}

WITH fhv_trips AS (
  SELECT 
    pickup_year
  , pickup_month
  , pickup_locationid
  , pickup_zone
  , pickup_datetime
  , dropoff_locationid
  , dropoff_zone
  , dropoff_datetime
  , TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, SECOND) AS trip_duration_sec
  FROM {{ ref('fact_fhv_trips') }}
)

, duration_percentiles AS (
  SELECT
    pickup_year
  , pickup_month
  , pickup_locationid
  , pickup_zone
  , pickup_datetime
  , dropoff_locationid
  , dropoff_zone
  , dropoff_datetime
  , trip_duration_sec
  , PERCENTILE_CONT(trip_duration_sec, 0.5) OVER(PARTITION BY pickup_year, pickup_month, pickup_locationid, dropoff_locationid) AS p50
  , PERCENTILE_CONT(trip_duration_sec, 0.9) OVER(PARTITION BY pickup_year, pickup_month, pickup_locationid, dropoff_locationid) AS p90
  , PERCENTILE_CONT(trip_duration_sec, 0.95) OVER(PARTITION BY pickup_year, pickup_month, pickup_locationid, dropoff_locationid) AS p95
  , PERCENTILE_CONT(trip_duration_sec, 0.97) OVER(PARTITION BY pickup_year, pickup_month, pickup_locationid, dropoff_locationid) AS p97 
  FROM fhv_trips
)

, final_data AS (
  SELECT 
    pickup_year
  , pickup_month
  , pickup_locationid
  , dropoff_locationid
  , pickup_zone
  , dropoff_zone 
  , COUNT(1) AS num_obs
  , MIN(trip_duration_sec) AS min_trip_duration_sec
  , AVG(trip_duration_sec) AS avg_trip_duration_sec
  , ANY_VALUE(p50) AS p50
  , ANY_VALUE(p90) AS p90
  , ANY_VALUE(p95) AS p95
  , ANY_VALUE(p97) AS p97
  , MAX(trip_duration_sec) AS max_trip_duration_sec
  FROM duration_percentiles
  GROUP BY 1,2,3,4,5,6
)

SELECT 
  pickup_year
, pickup_month
, pickup_zone
, dropoff_zone 
, num_obs
, min_trip_duration_sec
, avg_trip_duration_sec
, p50
, p90
, p95
, p97
, max_trip_duration_sec
FROM final_data 
WHERE 1=1