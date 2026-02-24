import logging
from pathlib import Path

from pyspark.sql import SparkSession, DataFrame

from base import BaseCollection
from enums import SeedType, DatasetType, FileExtensionType
from schemas import Field


class Seed(BaseCollection):

    def __init__(self, url: str,
                 fields: list[Field],
                 collection_type: DatasetType | SeedType,
                 file_extension_type: FileExtensionType) -> None:
        super().__init__(url, collection_type, fields, file_extension_type)

    @property
    def name(self) -> str:
        return f"{self.collection_type.value}"

    def run(self, session: SparkSession,
            directory_path: Path,
            chunk_size: int = 0,
            number_of_partitions: int = 1
            ) -> DataFrame | None:
        try:
            df: DataFrame = self.fetch_data(session, directory_path, chunk_size)
            df: DataFrame = self.process_data(df)
            return df

        except Exception as e:
            logging.error(f"Failed to process {self.name}: {e}")
