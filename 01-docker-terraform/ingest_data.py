import argparse
import logging
from time import time

import pandas as pd
from sqlalchemy import create_engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Ingest data from CSV to PostgreSQL')

    parser.add_argument('--user', type=str, help='PostgreSQL user', required=True)
    parser.add_argument('--password', type=str, help='PostgreSQL password', required=True)
    parser.add_argument('--host', type=str, help='PostgreSQL host', required=True)
    parser.add_argument('--port', type=int, help='PostgreSQL port', required=True)
    parser.add_argument('--db_name', type=str, help='PostgreSQL database name', required=True)
    parser.add_argument('--file_path', type=str, help='Path to CSV file', required=True)
    parser.add_argument('--table_name', type=str, help='Table name', required=True)
    parser.add_argument('--chunksize', type=int, help='Chunk size', required=True)

    return parser.parse_args()
  

def ingest_data(params: argparse.Namespace) -> None:
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    csv_path = params.file_path
    table_name = params.table_name
    chunksize = params.chunksize

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    try:
        df_iter = pd.read_csv(csv_path, iterator=True, chunksize=chunksize)
        
        df = next(df_iter)
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
        
        pd.io.sql.get_schema(df, table_name, con=engine)
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        total_rows = len(df)
        logging.info(f'First chunk inserted: {len(df)} rows')

        while True:
            try:
                t_start = time()
                
                df = next(df_iter)
                df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
                df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
                
                df.to_sql(table_name, engine, if_exists='append', index=False)
                
                t_end = time()
                total_rows += len(df)
                
                logging.info(f'Chunk loaded in {t_end - t_start:.2f} seconds. Total rows: {total_rows}')
                
            except StopIteration:
                logging.info(f'Finished ingesting data. Total rows: {total_rows}')
                break
                
    except Exception as e:
        logging.error(f'Error while ingesting data: {e}')
        raise


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    params = parse_args()
    ingest_data(params)
    logging.info('Data ingestion completed')


if __name__ == '__main__':
    main()