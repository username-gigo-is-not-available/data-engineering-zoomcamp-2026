"""@bruin
name: ingestion.trips
type: python
image: python:3.13
materialization:
  type: table
  strategy: append
connection: data-engineering-zoomcamp-2026-nyc-taxi
@bruin"""
import json
import logging
import os
from datetime import datetime, date
import pyarrow as pa
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.datasets import Dataset
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.enums import DatasetType
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.schemas import Field, SCHEMA
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.settings import ApplicationSettings
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.utils import DateTimeUtils

logging.basicConfig(level=logging.INFO)

def materialize():

    logging.info(f"Ingestion started {datetime.now()}")
    pa.util.download_tzdata_on_windows()
    variables: dict[str, str] = json.loads(os.environ.get("BRUIN_VARS", "{}"))

    start_date: date = DateTimeUtils.parse_date(os.environ.get("BRUIN_START_DATE", "2019-01-01"))
    end_date: date = DateTimeUtils.parse_date(os.environ.get("BRUIN_END_DATE", "2019-02-01"))
    date_range: list[date] = DateTimeUtils.generate_date_range(start_date, end_date)

    dataset_types: list[DatasetType] = [DatasetType.from_str(d) for d in variables.get("datasets", ["green", "yellow"])]
    tables: list[pa.Table] = []
    extraction_time = datetime.now()
    schema: list[Field] = SCHEMA
    for dt in date_range:
        year = dt.year
        month = dt.month
        for dataset_type in dataset_types:

            url: str = ApplicationSettings.NYC_TAXI_URL.format(dataset_type=dataset_type, year=year,
                                                               month=f"{month:02d}")

            dataset: Dataset = Dataset(
                url=url,
                type=dataset_type,
                year=year,
                month=month,
                columns=schema
            )

            table: pa.Table = dataset.run()
            if not table:
                logging.error(f"Failed to create table for dataset {dataset.name}")
                break

            row_count: int = table.num_rows
            table = table.append_column("extracted_at", pa.array([extraction_time] * row_count))
            table = table.append_column("dataset_source", pa.array([dataset_type.value] * row_count))
            tables.append(table)

    logging.info(f"Ingestion finished {datetime.now()}")
    return pa.concat_tables(tables, promote_options="permissive").to_pandas()


# if __name__ == '__main__':
#     materialize()
