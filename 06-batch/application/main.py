import logging
from datetime import date
from pathlib import Path

from pyspark.sql import SparkSession, DataFrame

from application.queries import least_frequent_pick_up_zone
from init import init_session, init_directories
from queries import count_trips_for_date, longest_trip_duration
from schemas import YELLOW_TAXI_FIELDS, TAXI_ZONE_FIELDS
from seeds import Seed
from datasets import Dataset
from enums import DatasetType, SeedType, FileExtensionType
from settings import ApplicationConfiguration, StorageConfiguration

logging.basicConfig(level=logging.INFO)


def main() -> None:
    session = None
    year: int = 2025
    month: int = 11
    trips_data_url: str = ApplicationConfiguration.NYC_TAXI_TRIPS_DATA_URL
    zones_data_url: str = ApplicationConfiguration.NYC_TAXI_ZONES_DATA_URL

    directory: Path = StorageConfiguration.DIRECTORY_PATH

    number_of_partitions: int = ApplicationConfiguration.NUMBER_OF_PARTITIONS
    chunk_size: int = ApplicationConfiguration.CHUNK_SIZE

    try:
        session: SparkSession = init_session()
        init_directories(paths=[
            directory
        ])

        yellow_dataset: Dataset = Dataset(
            url=trips_data_url,
            collection_type=DatasetType.YELLOW,
            year=year,
            month=month,
            fields=YELLOW_TAXI_FIELDS,
            file_extension_type=FileExtensionType.PARQUET
        )

        df_yellow: DataFrame = yellow_dataset.run(
            session=session,
            directory_path=directory,
            chunk_size=chunk_size,
            number_of_partitions=number_of_partitions
        )

        zones_seed: Seed = Seed(
            url=zones_data_url,
            collection_type=SeedType.ZONES,
            fields=TAXI_ZONE_FIELDS,
            file_extension_type=FileExtensionType.CSV
        )

        df_zones: DataFrame = zones_seed.run(
            session=session,
            directory_path=directory,
            chunk_size=chunk_size,
        )


        logging.info(f"Count total trips 2025-11-15: {count_trips_for_date(df_yellow, date(year, month, 15))}")
        logging.info(f"Longest trip duration (hours): {longest_trip_duration(df_yellow)}")
        logging.info(f"Least frequent pick up zone: {least_frequent_pick_up_zone(df_yellow, df_zones)}")

        yellow_dataset_partitioned_path: Path = directory / Path("_".join([yellow_dataset.name, "partitioned"]))
        df_yellow.write.parquet(str(yellow_dataset_partitioned_path), mode="overwrite")
        logging.info(Dataset.average_partitioned_file_size(yellow_dataset_partitioned_path))

    except Exception as e:
        logging.error(e)
    finally:
        session.stop()


if __name__ == '__main__':
    main()
