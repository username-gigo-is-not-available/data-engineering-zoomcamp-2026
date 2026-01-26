from dataclasses import dataclass
from pathlib import Path
import logging

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from sqlalchemy import Engine
from enums import FileType, TableExistsStrategyType
import pyarrow.csv as pv
from settings import StorageConfiguration


@dataclass(frozen=True)
class Column:
    source_column_name: str
    destination_column_name: str
    data_type: pa.DataType

@dataclass
class Dataset:
    url: str
    name: str
    columns: list[Column]

    @property
    def schema(self) -> pa.Schema:
        return pa.schema([(c.destination_column_name, c.data_type) for c in self.columns])

    @property
    def columns_map(self) -> dict:
        return {c.source_column_name: c.destination_column_name for c in self.columns}

    @classmethod
    def get_if_exists_strategy_type(cls, index: int):
        return TableExistsStrategyType.REPLACE if index == 0 else TableExistsStrategyType.APPEND

    def path(self, output_directory: Path) -> Path:
        return output_directory / Path(self.name).with_suffix(FileType.PARQUET.extension)

    def to_parquet(self, output_directory: Path):

        if self.url.endswith(FileType.CSV.extension):
            table: pa.Table = pv.read_csv(self.path(output_directory)).rename_columns(self.columns_map).cast(self.schema)
            pq.write_table(table, self.path(output_directory))
            logging.info(f"Successfully converted {self.url} to {FileType.PARQUET.extension}")

    def fetch_data(self,
                   output_directory: Path,
                   chunk_size: int) -> None:
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                file_path: Path = self.path(output_directory)

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)

                logging.info(f"Successfully downloaded {self.url}")
        except Exception as e:
            logging.error(f"Failed to download {self.url}: {e}")

    def store_data(self,
                   input_directory: Path,
                   engine: Engine,
                   chunk_size: int) -> None:
        file: pq.ParquetFile = pq.ParquetFile(self.path(input_directory))
        for idx, chunk in enumerate(file.iter_batches(batch_size=chunk_size)):
            df: pd.DataFrame = chunk.to_pandas().rename(columns=self.columns_map)
            strategy: TableExistsStrategyType = self.get_if_exists_strategy_type(idx)
            try:
                # TODO: complains about enum -> literal
                df.to_sql(name=self.name, con=engine, if_exists=strategy, chunksize=chunk_size, index=False) # noqa -
                logging.info(f"Successfully stored chunk {idx} from dataset {self.name} to database {StorageConfiguration.DATABASE_NAME}")
            except Exception as e:
                logging.error(f"Failed to store chunk {idx} from dataset {self.name} to database {StorageConfiguration.DATABASE_NAME}: {e}")