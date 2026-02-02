import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator, Any

import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import Engine, MetaData, Table, delete, insert

from common.enums import DatasetType, FileType
from common.settings import StorageConfiguration
from common.utils import DateTimeUtils


@dataclass
class Dataset:
    type: DatasetType
    month: int
    year: int

    @property
    def name(self) -> str:
        return f"{self.type.value}_{self.year}_{self.month:02d}"

    def delete_existing_data(self,
                             table: Table,
                             engine: Engine) -> None:
        start_date = DateTimeUtils.start_of_month(self.year, self.month)
        end_date = DateTimeUtils.end_of_month(start_date)
        stmt = delete(table).where(
            table.c.pick_up_datetime.between(start_date, end_date)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            logging.info(f"Deleted {result.rowcount} records for {self.name}")

    def path(self, directory_path: Path) -> Path:
        return directory_path / Path(self.name).with_suffix(FileType.PARQUET.extension)

    def read_chunk(self, file_path: Path, chunk_size: int) -> Iterator[pa.RecordBatch]:
        file = pq.ParquetFile(file_path)
        for chunk in file.iter_batches(batch_size=chunk_size):
            yield chunk

    def store_chunk(self, chunk: pa.RecordBatch,
                    table: Table,
                    engine: Engine) -> None:
        data: list[Any] = chunk.to_pylist()
        stmt = insert(table)

        with engine.connect() as conn:
            conn.execute(stmt, data)
            conn.commit()

    def run(self,
            input_path: Path,
            engine: Engine,
            chunk_size: int) -> None:

        metadata = MetaData()
        table: Table = Table(self.type.value, metadata, autoload_with=engine)
        self.delete_existing_data(table=table, engine=engine)
        chunks = self.read_chunk(input_path, chunk_size)

        number_of_rows = 0

        for idx, chunk in enumerate(chunks):
            try:
                self.store_chunk(chunk=chunk, table=table, engine=engine)
                number_of_rows += chunk.num_rows
                logging.info(
                    f"Successfully stored chunk {idx} from dataset {self.name} to database {StorageConfiguration.DATABASE_NAME}")
            except Exception as e:
                logging.error(
                    f"Failed to store chunk {idx} from dataset {self.name} to database {StorageConfiguration.DATABASE_NAME}: {e}")

        logging.info(f"Loaded {number_of_rows} records for {self.name}")