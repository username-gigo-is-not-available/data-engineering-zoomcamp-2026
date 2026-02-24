import pyarrow as pa
from dataclasses import dataclass
from data_platforms.taxi_rides_ny.pipeline.assets.ingestion.enums import DatasetType


@dataclass(frozen=True)
class Field:
    source_column_name: str
    destination_column_name: str
    data_type: pa.DataType


GREEN_TAXI_TYPE_COLUMNS: list[Field] = [
    Field('VendorID', 'vendor_id', pa.int64()),
    Field('lpep_pickup_datetime', 'pick_up_datetime', pa.timestamp('ns')),
    Field('lpep_dropoff_datetime', 'drop_off_datetime', pa.timestamp('ns')),
    Field('store_and_fwd_flag', 'store_and_forward_flag', pa.string()),
    Field('RatecodeID', 'rate_code_id', pa.int64()),
    Field('PULocationID', 'pick_up_location_id', pa.int64()),
    Field('DOLocationID', 'drop_off_location_id', pa.int64()),
    Field('passenger_count', 'passenger_count', pa.int64()),
    Field('trip_distance', 'trip_distance', pa.float64()),
    Field('fare_amount', 'fare_amount', pa.float64()),
    Field('extra', 'extra', pa.float64()),
    Field('mta_tax', 'mta_tax', pa.float64()),
    Field('tip_amount', 'tip_amount', pa.float64()),
    Field('tolls_amount', 'tolls_amount', pa.float64()),
    Field('ehail_fee', 'ehail_fee', pa.float64()),
    Field('improvement_surcharge', 'improvement_surcharge', pa.float64()),
    Field('total_amount', 'total_amount', pa.float64()),
    Field('payment_type', 'payment_type_id', pa.int64()),
    Field('trip_type', 'trip_type', pa.int64()),
    Field('congestion_surcharge', 'congestion_surcharge', pa.float64())
]

YELLOW_TAXI_TYPE_COLUMNS: list[Field] = [
    Field('VendorID', 'vendor_id', pa.int64()),
    Field('tpep_pickup_datetime', 'pick_up_datetime', pa.timestamp('ns')),
    Field('tpep_dropoff_datetime', 'drop_off_datetime', pa.timestamp('ns')),
    Field('passenger_count', 'passenger_count', pa.int64()),
    Field('trip_distance', 'trip_distance', pa.float64()),
    Field('RatecodeID', 'rate_code_id', pa.int64()),
    Field('store_and_fwd_flag', 'store_and_forward_flag', pa.string()),
    Field('PULocationID', 'pick_up_location_id', pa.int64()),
    Field('DOLocationID', 'drop_off_location_id', pa.int64()),
    Field('payment_type', 'payment_type_id', pa.int64()),
    Field('fare_amount', 'fare_amount', pa.float64()),
    Field('extra', 'extra', pa.float64()),
    Field('mta_tax', 'mta_tax', pa.float64()),
    Field('tip_amount', 'tip_amount', pa.float64()),
    Field('tolls_amount', 'tolls_amount', pa.float64()),
    Field('improvement_surcharge', 'improvement_surcharge', pa.float64()),
    Field('total_amount', 'total_amount', pa.float64()),
    Field('congestion_surcharge', 'congestion_surcharge', pa.float64())
]

SCHEMA_MAP: dict[DatasetType, list[Field]] = {
    DatasetType.GREEN: GREEN_TAXI_TYPE_COLUMNS,
    DatasetType.YELLOW: YELLOW_TAXI_TYPE_COLUMNS,
}

all_fields = set([field for fields_list in SCHEMA_MAP.values() for field in fields_list])
SCHEMA: list[Field] = list(all_fields)