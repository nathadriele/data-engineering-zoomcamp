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

        create_table(conn, color)
        import_data(data, conn, TABLES[color])
        data.close()
        mark_as_inserted(conn, color, year, month)
        conn.commit()
        print("Transaction complete")


def create_table(conn, color: str):
    cursor = conn.cursor()
    cursor.execute(CREATE_TAXI_TABLE[color])


def already_inserted(conn, color: str, year: int, month: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(CREATE_INSERTED_TABLE)
    cursor.execute(
        f"select 1 from {INSERTED_DATA} where color='{color}' AND year={year} AND month={month}"
    )
    return cursor.fetchone() is not None


def mark_as_inserted(conn, color: str, year: int, month: int) -> None:
    cursor = conn.cursor()
    cursor.execute(
        f"insert into {INSERTED_DATA}(color, year, month) VALUES('{color}', {year}, {month})"
    )
    print(f"inserted {color}, {year}, {month}")


def create_connection():
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "example")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_DB", "taxi")

    return psycopg2.connect(f"postgresql://{user}:{password}@{host}:{port}/{db}")


def read_url_data(color: str, year: int, month: int):
    temp_file = tempfile.TemporaryFile()
    assert 1 <= month <= 12
    assert color in TABLES.keys()
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_{year:04d}-{month:02d}.csv.gz"
    response = requests.get(url, stream=True)
    response.raise_for_status()
    for chunk in response.iter_content(chunk_size=1024):
        temp_file.write(chunk)
    print("downloaded data from %s into %s" % (url, temp_file.name))
    temp_file.seek(0) 
    return temp_file
