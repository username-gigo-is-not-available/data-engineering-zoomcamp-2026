import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    NYC_TAXI_TRIPS_DATA_URL: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_type}_tripdata_{year}-{month}.parquet"
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_NAME: str = os.getenv("KAFKA_TOPIC_NAME", "green-trips")

class StorageConfig:
    DIRECTORY_PATH: Path = Path(os.getenv("DIRECTORY_PATH", "../data"))
    DATABASE_HOST: str = os.getenv("POSTGRES_HOST")
    DATABASE_PORT_NUMBER: int = int(os.getenv("POSTGRES_PORT"))
    DATABASE_USERNAME: str = os.getenv("POSTGRES_USER")
    DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DATABASE_NAME: str = os.getenv("POSTGRES_DB")

    DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT_NUMBER}/{DATABASE_NAME}'