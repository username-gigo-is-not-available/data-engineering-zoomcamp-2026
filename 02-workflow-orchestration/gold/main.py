import logging
from pathlib import Path

import click
from sqlalchemy import Engine, create_engine

from common.cli import dataset_options
from common.enums import DatasetType
from common.settings import StorageConfiguration
from gold.datasets import Dataset

logging.basicConfig(level=logging.INFO)


@click.command()
@dataset_options
@click.option('--file_path', type=click.Path(exists=True), help='Direct path to the parquet file')

def main(dataset_type: str, year: int, month: int, chunk_size: int, file_path: Path) -> None:
    try:
        engine: Engine = create_engine(StorageConfiguration.DATABASE_URL)
        engine.connect()
    except Exception as e:
        logging.error(f"Initialization failed: {e}")
        return

    dataset_type: DatasetType = DatasetType.from_str(dataset_type)
    dataset: Dataset = Dataset(
        type=dataset_type,
        year=year,
        month=month,
    )

    input_path: Path = file_path if file_path else dataset.path(StorageConfiguration.DIRECTORY_PATH)

    dataset.run(
        input_path=input_path,
        engine=engine,
        chunk_size=chunk_size,
    )


if __name__ == '__main__':
    main()
