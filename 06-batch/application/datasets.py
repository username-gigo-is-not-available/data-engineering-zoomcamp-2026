import logging
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql.connect.session import SparkSession
from pyspark.sql import functions as F

from enums import DatasetType, FileExtensionType, SeedType
from schemas import Field
from base import BaseCollection


class Dataset(BaseCollection):

    def __init__(self, url: str,
                 year: int,
                 month: int,
                 fields: list[Field],
                 collection_type: DatasetType,
                 file_extension_type: FileExtensionType,
                 ) -> None:
        super().__init__(url, collection_type, fields, file_extension_type)
        self.url = url.format(dataset_type=collection_type,
                              year=year,
                              month=month)
        self.year = year
        self.month = month

    @property
    def name(self) -> str:
        return f"{self.collection_type.value}_{self.year}_{self.month}"

    def filter_data(self, df: DataFrame) -> DataFrame:
        return df.filter(
            (F.year(F.col("pick_up_datetime")) == int(self.year)) &
            (F.month(F.col("pick_up_datetime")) == int(self.month))
        )

    def partition_data(self, df: DataFrame, number_of_partitions: int) -> DataFrame:
        return df.repartition(number_of_partitions)

    def run(self, session: SparkSession,
            directory_path: Path,
            chunk_size: int = 0,
            number_of_partitions: int = 0
            ) -> DataFrame | None:

        try:
            df: DataFrame = self.fetch_data(session, directory_path, chunk_size)
            df: DataFrame = self.process_data(df)
            df: DataFrame = self.filter_data(df)
            df: DataFrame = self.partition_data(df, number_of_partitions)
            return df

        except Exception as e:
            logging.error(f"Failed to process {self.name}: {e}")
