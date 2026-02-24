import os
from pathlib import Path


class ApplicationConfiguration:
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 100_000))
    NUMBER_OF_PARTITIONS: int = int(os.getenv("NUMBER_OF_PARTITIONS", 4))
    NYC_TAXI_TRIPS_DATA_URL: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_type}_tripdata_{year}-{month}.parquet"
    NYC_TAXI_ZONES_DATA_URL: str = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

class StorageConfiguration:
    DIRECTORY_PATH: Path = Path(os.getenv("DIRECTORY_PATH", "../data"))
