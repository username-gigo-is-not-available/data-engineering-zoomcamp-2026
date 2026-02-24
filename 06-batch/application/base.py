import logging
from pathlib import Path

import requests
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField
from pyspark.sql import functions as F

from enums import DatasetType, SeedType, FileExtensionType
from schemas import Field


class BaseCollection:

    def __init__(self,
                 url: str,
                 collection_type: DatasetType | SeedType,
                 fields: list[Field],
                 file_extension_type: FileExtensionType
                 ):

        self.url = url
        self.collection_type = collection_type
        self.fields = fields
        self.file_extension_type = file_extension_type

    @property
    def source_schema(self) -> StructType:
        return StructType([
            StructField(f.source_column_name, f.data_type, True) for f in self.fields
        ]
        )

    @property
    def destination_schema(self) -> StructType:
        return StructType([
            StructField(f.destination_column_name, f.data_type, True) for f in self.fields
        ]
        )

    @property
    def columns_map(self) -> dict:
        return {c.source_column_name: c.destination_column_name for c in self.fields}

    @property
    def name(self):
        raise NotImplementedError

    def path(self, directory: Path) -> Path:
        return directory / Path(f"{self.name}.{self.file_extension_type.value}")

    def read_data(self, session: SparkSession, directory_path: Path):
        file_path: str = str(self.path(directory_path))
        if self.file_extension_type == FileExtensionType.CSV:
            return (
                session
                .read.option("header", True)
                .schema(self.source_schema)
                .csv(file_path)
            )
        elif self.file_extension_type == FileExtensionType.PARQUET:
            return (
                session
                .read
                .parquet(file_path)
            )
        else:
            raise NotImplementedError

    @staticmethod
    def average_partitioned_file_size(path: Path):
        total_bytes: float = sum(f.stat().st_size for f in Path(path).glob('**/*.parquet'))
        num_files: int = len(list(Path(path).glob('**/*.parquet')))
        logging.info(f"Total Disk Size: {total_bytes / (1024 * 1024):.2f} MB")
        logging.info(f"Average File Size per Partition: {(total_bytes / num_files) / (1024 * 1024):.2f} MB")

    def fetch_data(self, session: SparkSession, directory_path: Path, chunk_size: int):
        file_path: str = str(self.path(directory_path))
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        file.write(chunk)

            return self.read_data(session, directory_path)

        except Exception as e:
            logging.error(f"Failed to fetch {self.name}: {e}")


    def process_data(self, df: DataFrame) -> DataFrame:
        try:
            for source, dest in self.columns_map.items():
                df = df.withColumnRenamed(source, dest)

            for field in self.fields:
                df = df.withColumn(
                    field.destination_column_name,
                    F.col(field.destination_column_name).cast(field.data_type)
                )

            logging.info(f"Successfully processed {self.name}")
            return df

        except Exception as e:
            logging.error(f"Failed to process {self.name}: {e}")
            raise e

    def run(self, session: SparkSession,
            directory_path: Path,
            chunk_size: int = 0,
            number_of_partitions: int = 0
            ) -> DataFrame | None:
        raise NotImplementedError
