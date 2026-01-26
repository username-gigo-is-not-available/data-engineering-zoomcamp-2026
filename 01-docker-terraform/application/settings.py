import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class ApplicationConfiguration:
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 100_000))
    NYC_TAXI_TRIPS_DATA_URL: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    NYC_TAXI_ZONES_DATA_URL: str = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


class StorageConfiguration:
    OUTPUT_DIRECTORY_PATH: Path = Path("../data")
    DATABASE_HOST: str = os.getenv("POSTGRES_HOST")
    DATABASE_PORT_NUMBER: int = int(os.getenv("POSTGRES_PORT"))
    DATABASE_USERNAME: str = os.getenv("POSTGRES_USER")
    DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DATABASE_NAME: str = os.getenv("POSTGRES_DB")

    DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT_NUMBER}/{DATABASE_NAME}'