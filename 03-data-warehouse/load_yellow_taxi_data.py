import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

import requests
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

# Change this to your bucket name
BUCKET_NAME = os.environ["BUCKET_NAME"]

# If you authenticated through the GCP SDK you can comment out these two lines
# CREDENTIALS_FILE = "gcs.json"
# client = storage.Client.from_service_account_json(CREDENTIALS_FILE)


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]


def transfer_file(month):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    file_name = f"yellow_tripdata_2024-{month}.parquet"
    blob = bucket.blob(file_name)

    url = f"{BASE_URL}{month}.parquet"
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with tempfile.TemporaryFile() as file:
            for chunk in response.iter_content(1024 * 8):
                file.write(chunk)
            blob.upload_from_file(file, rewind=True)
    print(f"uploaded {month}.")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(transfer_file, MONTHS))

    print("All files processed and verified.")