import logging
import click

from common.cli import dataset_options
from common.settings import StorageConfiguration, ApplicationConfiguration
from silver.datasets import Dataset
from common.schemas import SCHEMA_MAP, Field
from common.enums import DatasetType

logging.basicConfig(level=logging.INFO)


@click.command()
@dataset_options
def main(dataset_type: str, year: int, month: int, chunk_size: int) -> None:


    try:
        StorageConfiguration.DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Initialization failed: {e}")
        return

    url: str = ApplicationConfiguration.NYC_TAXI_TRIPS_DATA_URL_TEMPLATE.format(
                dataset=dataset_type,
                month=f"{month:02d}",
                year=year,
        )

    dataset_type: DatasetType = DatasetType.from_str(dataset_type)
    schema: list[Field] = SCHEMA_MAP[dataset_type]

    dataset: Dataset = Dataset(
        url=url,
        type=dataset_type,
        year=year,
        month=month,
        columns=schema
    )

    dataset.run(
        directory_path=StorageConfiguration.DIRECTORY_PATH,
        chunk_size=chunk_size,
        date_column=ApplicationConfiguration.DATETIME_COLUMN
    )

if __name__ == '__main__':
    main()