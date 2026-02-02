from sqlalchemy import create_engine, MetaData, Table, Column, Engine
from common.schemas import SCHEMA_MAP
from common.settings import StorageConfiguration

import logging

logging.basicConfig(level=logging.INFO)

def setup_database():
    try:

        engine: Engine = create_engine(StorageConfiguration.DATABASE_URL)
        metadata: MetaData = MetaData()

        for dataset_type, columns in SCHEMA_MAP.items():

            sql_cols = [
                Column(col.destination_column_name, col.sqlalchemy_data_type)
                for col in columns
            ]

            Table(dataset_type.value, metadata, *sql_cols)

        metadata.create_all(engine)

        logging.info("Database setup complete!")

    except Exception as e:
        logging.error(f"Database setup failed: {e}")

if __name__ == "__main__":
    setup_database()