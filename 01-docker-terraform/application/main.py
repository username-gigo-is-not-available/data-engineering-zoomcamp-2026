import logging

import pyarrow as pa
from sqlalchemy import create_engine, Engine
from datasets import Dataset, Column
from settings import StorageConfiguration, ApplicationConfiguration

logging.basicConfig(level=logging.INFO)


def main() -> None:

    try:
        StorageConfiguration.OUTPUT_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        engine: Engine = create_engine(StorageConfiguration.DATABASE_URL)

    except Exception as e:
        logging.error(e)
        return

    trips = Dataset(url=ApplicationConfiguration.NYC_TAXI_TRIPS_DATA_URL, name="trips",
                    columns=
                    [
                        Column('VendorID', 'vendor_id', pa.int64()),
                        Column('lpep_pickup_datetime', 'pick_up_datetime', pa.timestamp('ns')),
                        Column('lpep_dropoff_datetime', 'drop_off_datetime', pa.timestamp('ns')),
                        Column('store_and_fwd_flag', 'store_and_fwd_flag', pa.string()),
                        Column('RatecodeID', 'rate_code_id', pa.int64()),
                        Column('PULocationID', 'pick_up_location_id', pa.int64()),
                        Column('DOLocationID', 'drop_off_location_id', pa.int64()),
                        Column('passenger_count', 'passenger_count', pa.int64()),
                        Column('trip_distance', 'trip_distance', pa.float64()),
                        Column('fare_amount', 'fare_amount', pa.float64()),
                        Column('extra', 'extra', pa.float64()),
                        Column('mta_tax', 'mta_tax', pa.float64()),
                        Column('tip_amount', 'tip_amount', pa.float64()),
                        Column('tolls_amount', 'tolls_amount', pa.float64()),
                        Column('ehail_fee', 'ehail_fee', pa.float64()),
                        Column('improvement_surcharge', 'improvement_surcharge', pa.float64()),
                        Column('total_amount', 'total_amount', pa.float64()),
                        Column('payment_type', 'payment_type', pa.int64()),
                        Column('trip_type', 'trip_type', pa.int64()),
                        Column('congestion_surcharge', 'congestion_surcharge', pa.float64())
                    ]
                    )

    zones = Dataset(url=ApplicationConfiguration.NYC_TAXI_ZONES_DATA_URL, name="zones",
                    columns=[
                        Column('LocationID', 'location_id', pa.int64()),
                        Column('Borough', 'borough', pa.string()),
                        Column('Zone', 'zone', pa.string()),
                        Column('service_zone', 'service_zone', pa.string())
                    ])

    for dataset in [trips, zones]:
        dataset.fetch_data(
            output_directory=StorageConfiguration.OUTPUT_DIRECTORY_PATH,
            chunk_size=ApplicationConfiguration.CHUNK_SIZE)
        dataset.to_parquet(
            StorageConfiguration.OUTPUT_DIRECTORY_PATH)
        dataset.store_data(
            input_directory=StorageConfiguration.OUTPUT_DIRECTORY_PATH,
            engine=engine,
            chunk_size=ApplicationConfiguration.CHUNK_SIZE)


if __name__ == '__main__':
    main()
