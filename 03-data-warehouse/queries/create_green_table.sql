CREATE TABLE IF NOT EXISTS green_trip (
    vendorid smallint,
    lpep_pickup_datetime timestamp NOT NULL,
    lpep_dropoff_datetime timestamp NOT NULL,
    store_and_fwd_flag boolean,
    ratecodeid smallint,
    pulocationid int,
    dolocationid int,
    passenger_count smallint,
    trip_distance numeric,
    fare_amount numeric,
    extra numeric,
    mta_tax numeric,
    tip_amount numeric,
    tolls_amount numeric,
    ehail_fee numeric,
    improvement_surcharge numeric,
    total_amount numeric,
    payment_type smallint,
    trip_type smallint,
    congestion_surcharge numeric,
    CONSTRAINT trip_unique UNIQUE (
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        pulocationid,
        dolocationid,
        fare_amount,
        trip_distance
    )
);