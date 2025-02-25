{{
    config(
        materialized='table'
    )
}}

WITH trip_data AS (
    SELECT 
      fhv.tripid
    , fhv.dispatching_base_num
    , fhv.affiliated_base_number

    , fhv.pickup_locationid
    , pu_zones.borough AS pickup_borough
    , pu_zones.zone AS pickup_zone

    , fhv.dropoff_locationid
    , do_zones.borough AS dropoff_borough
    , do_zones.zone AS dropoff_zone

    , fhv.pickup_datetime
    , fhv.dropoff_datetime

    , EXTRACT(MONTH FROM fhv.pickup_datetime) AS pickup_month
    , CONCAT('Q', CAST(EXTRACT(QUARTER FROM fhv.pickup_datetime) AS STRING)) AS pickup_quarter
    , EXTRACT(YEAR FROM fhv.pickup_datetime) AS pickup_year

    , fhv.sr_flag
    , 'fhv' AS service_type
    , ROW_NUMBER() OVER(PARTITION BY fhv.tripid ORDER BY fhv.pickup_datetime) AS r
    FROM {{ ref('stg_fhv_tripdata') }} fhv
    INNER JOIN {{ ref('dim_zones') }} AS pu_zones
      ON fhv.pickup_locationid = pu_zones.locationid AND pu_zones.borough != 'Unknown'
    INNER JOIN {{ ref('dim_zones') }} AS do_zones
      ON fhv.dropoff_locationid = do_zones.locationid AND do_zones.borough != 'Unknown'
)

SELECT *
FROM trip_data
WHERE 1=1
      AND r = 1