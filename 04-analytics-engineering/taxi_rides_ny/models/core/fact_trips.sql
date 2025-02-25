{{
    config(
        materialized = 'table'
    )
}}

WITH green_tripdata AS (
    SELECT 
      *
    , 'Green' AS service_type
    FROM {{ ref('stg_green_tripdata') }}
    WHERE 1=1
)

, yellow_tripdata AS (
    SELECT *
    , 'Yellow' AS service_type
    FROM {{ ref('stg_yellow_tripdata') }}
    WHERE 1=1
)

, trips_unioned AS (
    SELECT 
      *
    FROM green_tripdata

    UNION ALL 

    SELECT 
      *
    FROM yellow_tripdata
)

SELECT 
  trips_unioned.tripid    
, trips_unioned.vendorid
, trips_unioned.service_type
, trips_unioned.ratecodeid

, trips_unioned.pickup_locationid
, pu_zones.borough AS pickup_borough
, pu_zones.zone AS pickup_zone

, trips_unioned.dropoff_locationid
, do_zones.borough AS dropoff_borough
, do_zones.zone AS dropoff_zone

/* Timestamps */
, trips_unioned.pickup_datetime
, trips_unioned.dropoff_datetime

/* Date info */
, EXTRACT(MONTH FROM trips_unioned.pickup_datetime) AS pickup_month
, CONCAT('Q', CAST(EXTRACT(QUARTER FROM trips_unioned.pickup_datetime) AS STRING)) AS pickup_quarter
, EXTRACT(YEAR FROM trips_unioned.pickup_datetime) AS pickup_year

/* Trip Information */
, trips_unioned.store_and_fwd_flag
, trips_unioned.passenger_count
, trips_unioned.trip_distance

, trips_unioned.trip_type

  /* Payment Information */
, trips_unioned.fare_amount
, trips_unioned.extra
, trips_unioned.mta_tax
, trips_unioned.tip_amount
, trips_unioned.tolls_amount
, trips_unioned.ehail_fee
, trips_unioned.improvement_surcharge
, trips_unioned.total_amount
, trips_unioned.payment_type
, trips_unioned.payment_type_description
FROM trips_unioned
INNER JOIN {{ ref('dim_zones') }} AS pu_zones 
  ON trips_unioned.pickup_locationid = pu_zones.locationid AND pu_zones.borough != 'Unknown'
INNER JOIN {{ ref('dim_zones') }} AS do_zones
  ON trips_unioned.dropoff_locationid = do_zones.locationid AND do_zones.borough != 'Unknown'
WHERE 1=1