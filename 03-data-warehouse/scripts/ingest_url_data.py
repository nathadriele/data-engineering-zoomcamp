import argparse
import gzip
import itertools
import os
import tempfile

import psycopg2
import requests

TABLES = {"green": "green_trip", "yellow": "yellow_trip"}
INSERTED_DATA = "inserted_data"
CREATE_INSERTED_TABLE = f"""
CREATE TABLE IF NOT EXISTS {INSERTED_DATA} (
    color text NOT NULL,
    year int NOT NULL,
    month int NOT NULL,
    CONSTRAINT unique_entry UNIQUE(color, year, month)
)
"""
CREATE_TAXI_TABLE = {
    "green": f"""
CREATE TABLE IF NOT EXISTS {TABLES['green']} (
  VendorID smallint,
  lpep_pickup_datetime timestamp not null,
  lpep_dropoff_datetime timestamp not null,
  store_and_fwd_flag boolean,
  RatecodeID smallint,
  PULocationID int,
  DOLocationID int,
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
  congestion_surcharge numeric
);
    """,
    "yellow": f"""
CREATE TABLE IF NOT EXISTS {TABLES['yellow']} (
  VendorID smallint,
  tpep_pickup_datetime timestamp not null,
  tpep_dropoff_datetime timestamp not null,
  passenger_count smallint,
  trip_distance numeric,
  RatecodeID smallint,
  store_and_fwd_flag boolean,
  PULocationID int,
  DOLocationID int,
  payment_type smallint,
  fare_amount numeric,
  extra numeric,
  mta_tax numeric,
  tip_amount numeric,
  tolls_amount numeric,
  improvement_surcharge numeric,
  total_amount numeric,
  congestion_surcharge numeric
  )
  ;
  """,
}


def get_taxi_data(color="green", year=2019, month=1):
    conn = create_connection()

    if already_inserted(conn, color, year, month):
        print(f"Already inserted {color}, {year}, {month}")
    else:
        try:
            data = read_url_data(color, year, month)
        except Exception:
            print(
                "Couldn't fetch data for color: %s, year: %d, month: %d"
                % (color, year, month)
            )
            return
