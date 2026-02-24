import io
import logging

import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
from dataclasses import dataclass

import requests

from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.enums import DatasetType
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.schemas import Field


@dataclass
class Dataset:
    url: str
    type: DatasetType
    month: int
    year: int
    columns: list[Field]

    @property
    def source_schema(self) -> pa.Schema:
        return pa.GREEN_TAXI_SCHEMA([(c.source_column_name, c.data_type) for c in self.columns])

    @property
    def destination_schema(self) -> pa.Schema:
        return pa.GREEN_TAXI_SCHEMA([(c.destination_column_name, c.data_type) for c in self.columns])

    @property
    def columns_map(self) -> dict:
        return {c.source_column_name: c.destination_column_name for c in self.columns}

    @property
    def name(self) -> str:
        return f"{self.type.value}_{self.year}_{self.month}"

    def fetch_data(self) -> pa.Table | None:
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                table = pq.read_table(io.BytesIO(response.content))
                logging.info(f"Successfully downloaded {self.url}")

                return table

        except Exception as e:
            logging.error(f"Failed to download {self.url}: {e}")
            return None

    def process_data(self, table: pa.Table) -> pa.Table:
        try:
            rename_dict = {k: v for k, v in self.columns_map.items() if k in table.column_names}
            table: pa.Table = table.rename_columns([rename_dict.get(n, n) for n in table.column_names])
            table = pa.Table.from_batches(table.to_batches())
            table: pa.Table = table.filter(
                pc.and_(
                    pc.equal(pc.year(table.column("pick_up_datetime")), int(self.year)
                             ),
                    pc.equal(pc.month(table.column("pick_up_datetime")), int(self.month)
                             )
                )
            )
            logging.info(f"Successfully processed {self.name}")
            return table
        except Exception as e:
            logging.error(f"Failed to process {self.name}: {e}")

    def run(self) -> pa.Table | None:

        try:
            table: pa.Table = self.fetch_data()
            return self.process_data(table)

        except Exception as e:
            logging.error(f"Failed to process {self.name}: {e}")
            return None
