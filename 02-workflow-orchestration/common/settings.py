import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class ApplicationConfiguration:
    NYC_TAXI_TRIPS_DATA_URL_TEMPLATE: str = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{dataset}/{dataset}_tripdata_{year}-{month}.csv.gz"
    DATETIME_COLUMN: str = "pick_up_datetime"

class StorageConfiguration:
    DIRECTORY_PATH: Path = Path(os.getenv("NYC_TAXI_DIRECTORY_PATH", "../data"))

    DATABASE_HOST: str = os.getenv("NYC_TAXI_DB_HOST")
    DATABASE_PORT_NUMBER: int = int(os.getenv("NYC_TAXI_DB_PORT"))
    DATABASE_USERNAME: str = os.getenv("NYC_TAXI_DB_USER")
    DATABASE_PASSWORD: str = os.getenv("NYC_TAXI_DB_PASSWORD")
    DATABASE_NAME: str = os.getenv("NYC_TAXI_DB_NAME")

    DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT_NUMBER}/{DATABASE_NAME}'