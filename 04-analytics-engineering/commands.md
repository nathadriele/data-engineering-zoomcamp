### Create Tables

```
CREATE OR REPLACE EXTERNAL TABLE `de-zc-hbg.ny_taxi.green_tripdata` (
      VendorID STRING,
      lpep_pickup_datetime TIMESTAMP,
      lpep_dropoff_datetime TIMESTAMP,
      store_and_fwd_flag STRING,
      RatecodeID STRING, 
      PULocationID STRING, 
      DOLocationID STRING, 
      passenger_count INT64, 
      trip_distance NUMERIC, 
      fare_amount NUMERIC, 
      extra NUMERIC, 
      mta_tax NUMERIC, 
      tip_amount NUMERIC, 
      tolls_amount NUMERIC, 
      ehail_fee NUMERIC, 
      improvement_surcharge NUMERIC, 
      total_amount NUMERIC, 
      payment_type STRING, 
      trip_type STRING, 
      congestion_surcharge NUMERIC
      
) OPTIONS (
    format ='CSV',
    compression = 'GZIP',
    uris = ['gs://de-zc-hbg-bucket/green/*.csv.gz'],
    skip_leading_rows = 1
    );

CREATE OR REPLACE EXTERNAL TABLE `de-zc-hbg.ny_taxi.yellow_tripdata` (
      VendorID STRING, 
      tpep_pickup_datetime TIMESTAMP, 
      tpep_dropoff_datetime TIMESTAMP, 
      passenger_count INT64, 
      trip_distance NUMERIC, 
      RatecodeID STRING, 
      store_and_fwd_flag STRING, 
      PULocationID STRING, 
      DOLocationID STRING, 
      payment_type STRING, 
      fare_amount NUMERIC, 
      extra NUMERIC, 
      mta_tax NUMERIC, 
      tip_amount NUMERIC, 
      tolls_amount NUMERIC, 
      improvement_surcharge NUMERIC, 
      total_amount NUMERIC, 
      congestion_surcharge NUMERIC

) OPTIONS (
    format ='CSV',
    compression = 'GZIP',
    uris = ['gs://de-zc-hbg-bucket/yellow/*.csv.gz'],
    skip_leading_rows = 1
    );

CREATE OR REPLACE EXTERNAL TABLE `de-zc-hbg.ny_taxi.fhv_tripdata` (
      dispatching_base_num STRING, 
      pickup_datetime TIMESTAMP, 
      dropOff_datetime TIMESTAMP, 
      PUlocationID STRING, 
      DOlocationID STRING, 
      SR_Flag STRING, 
      Affiliated_base_number STRING
) OPTIONS (
    format ='CSV',
    compression = 'GZIP',
    uris = ['gs://de-zc-hbg-bucket/fhv/*.csv.gz'],
    skip_leading_rows = 1
    );
```

### Dbt Command

```
dbt compile --select "q2"

dbt compile --select "q2" --vars '{'days_back': '1000'}'

dbt compile --select "q2" --vars '{'DBT_DAYS_BACK': '1000'}'
```
