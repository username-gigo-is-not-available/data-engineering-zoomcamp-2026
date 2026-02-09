import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from google.cloud import storage
import time

load_dotenv()

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 6))
DIRECTORY_PATH = os.getenv("DIRECTORY_PATH", "")
CHUNK_SIZE = os.getenv("CHUNK_SIZE", 100_000)

GCS_CLIENT = storage.Client(project=PROJECT_ID)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]


os.makedirs(DIRECTORY_PATH, exist_ok=True)

GCS_BUCKET = GCS_CLIENT.bucket(BUCKET_NAME)


def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DIRECTORY_PATH, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=GCS_BUCKET, name=blob_name).exists(GCS_CLIENT)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = GCS_BUCKET.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        file_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")