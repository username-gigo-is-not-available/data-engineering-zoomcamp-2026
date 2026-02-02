import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import gzip
import shutil
import io
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pyarrow.compute as pc
import requests

from common.enums import DatasetType, FileType, CompressionType
from common.schemas import Field
from common.utils import DateTimeUtils


@dataclass
class Dataset:
    url: str
    type: DatasetType
    month: int
    year: int
    columns: list[Field]

    @property
    def source_schema(self) -> pa.Schema:
        return pa.schema([(c.source_column_name, c.pyarrow_data_type) for c in self.columns])

    @property
    def destination_schema(self) -> pa.Schema:
        return pa.schema([(c.destination_column_name, c.pyarrow_data_type) for c in self.columns])

    @property
    def columns_map(self) -> dict:
        return {c.source_column_name: c.destination_column_name for c in self.columns}

    @property
    def name(self) -> str:
        return f"{self.type.value}_{self.year}_{self.month}"

    def csv_gz_path(self, directory_path: Path) -> Path:
        return directory_path / Path(self.name).with_suffix(FileType.CSV.extension + CompressionType.GZ.extension)

    def csv_path(self, directory_path: Path) -> Path:
        return directory_path / Path(self.name).with_suffix(FileType.CSV.extension)

    def parquet_path(self, directory_path: Path):
        return directory_path / Path(self.name).with_suffix(FileType.PARQUET.extension)

    def fetch_data(self,
                   output_path: Path,
                   chunk_size: int) -> None:
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()

                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)

                logging.info(f"Successfully downloaded {self.url}")
        except Exception as e:
            logging.error(f"Failed to download {self.url}: {e}")

    def uncompressed_file_size(self, input_path: Path):
        with gzip.open(input_path, 'rb') as f_in:
            with io.BytesIO() as f_out:
                shutil.copyfileobj(f_in, f_out)
                size_bytes = f_out.tell()

        logging.info(f"Uncompressed size: {size_bytes / (1024 ** 2):.1f} MiB")

    def read_batch(self, input_path: Path):
        convert_options = pv.ConvertOptions(
            column_types=self.source_schema,
            null_values=["", "NULL", "0", "nan", "NaN", "null"],
            strings_can_be_null=True
        )
        with pv.open_csv(input_path, convert_options=convert_options) as reader:
            for batch in reader:
                yield batch

    def rename_columns_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        return batch.rename_columns(self.columns_map)

    def cast_to_schema_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        return batch.cast(self.destination_schema)

    def filter_batch(self, batch: pa.RecordBatch, column: str) -> pa.RecordBatch:
        year_mask: list[bool] = pc.equal(pc.year(batch.column(column)), int(self.year))
        month_mask: list[bool] = pc.equal(pc.month(batch.column(column)), int(self.month))
        final_mask: list[bool] = pc.and_(year_mask, month_mask)

        return batch.filter(final_mask)

    def run(self,
            directory_path: Path,
            chunk_size: int,
            date_column: str
            ) -> None:

        csv_gz_path: Path = self.csv_gz_path(directory_path)
        parquet_path: Path = self.parquet_path(directory_path)
        try:
            self.fetch_data(csv_gz_path, chunk_size=chunk_size)
            self.uncompressed_file_size(csv_gz_path)
            with pq.ParquetWriter(parquet_path, self.destination_schema) as writer:
                for index, batch in enumerate(self.read_batch(csv_gz_path)):
                    batch: pa.RecordBatch = self.rename_columns_batch(batch)
                    batch: pa.RecordBatch = self.cast_to_schema_batch(batch)
                    batch: pa.RecordBatch = self.filter_batch(batch, date_column)
                    writer.write_batch(batch)
                    logging.info(
                        f"Successfully converted batch: {index} from {csv_gz_path.name} to {parquet_path.name}")

            logging.info(f"Successfully converted {self.name}")

        except Exception as e:
            logging.error(f"Failed to convert {self.name}: {e}")
