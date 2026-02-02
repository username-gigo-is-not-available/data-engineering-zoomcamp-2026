from dataclasses import dataclass

import pyarrow as pa
from sqlalchemy import BigInteger, Float, String, DateTime
from sqlalchemy.sql.type_api import TypeEngine

from common.enums import DatasetType

@dataclass(frozen=True)
class Field:
    source_column_name: str
    destination_column_name: str
    pyarrow_data_type: pa.DataType
    sqlalchemy_data_type: TypeEngine

GREEN_TAXI_COLUMNS: list[Field] = [
    Field('VendorID', 'vendor_id', pa.int64(), BigInteger()),
    Field('lpep_pickup_datetime', 'pick_up_datetime', pa.timestamp('ns'), DateTime()),
    Field('lpep_dropoff_datetime', 'drop_off_datetime', pa.timestamp('ns'), DateTime()),
    Field('store_and_fwd_flag', 'store_and_fwd_flag', pa.string(), String()),
    Field('RatecodeID', 'rate_code_id', pa.int64(), BigInteger()),
    Field('PULocationID', 'pick_up_location_id', pa.int64(), BigInteger()),
    Field('DOLocationID', 'drop_off_location_id', pa.int64(), BigInteger()),
    Field('passenger_count', 'passenger_count', pa.int64(), BigInteger()),
    Field('trip_distance', 'trip_distance', pa.float64(), Float()),
    Field('fare_amount', 'fare_amount', pa.float64(), Float()),
    Field('extra', 'extra', pa.float64(), Float()),
    Field('mta_tax', 'mta_tax', pa.float64(), Float()),
    Field('tip_amount', 'tip_amount', pa.float64(), Float()),
    Field('tolls_amount', 'tolls_amount', pa.float64(), Float()),
    Field('ehail_fee', 'ehail_fee', pa.float64(), Float()),
    Field('improvement_surcharge', 'improvement_surcharge', pa.float64(), Float()),
    Field('total_amount', 'total_amount', pa.float64(), Float()),
    Field('payment_type', 'payment_type', pa.int64(), BigInteger()),
    Field('trip_type', 'trip_type', pa.int64(), BigInteger()),
    Field('congestion_surcharge', 'congestion_surcharge', pa.float64(), Float())
]

YELLOW_TAXI_COLUMNS: list[Field] = [
    Field('VendorID', 'vendor_id', pa.int64(), BigInteger()),
    Field('tpep_pickup_datetime', 'pick_up_datetime', pa.timestamp('ns'), DateTime()),
    Field('tpep_dropoff_datetime', 'drop_off_datetime', pa.timestamp('ns'), DateTime()),
    Field('passenger_count', 'passenger_count', pa.int64(), BigInteger()),
    Field('trip_distance', 'trip_distance', pa.float64(), Float()),
    Field('RatecodeID', 'rate_code_id', pa.int64(), BigInteger()),
    Field('store_and_fwd_flag', 'store_and_fwd_flag', pa.string(), String()),
    Field('PULocationID', 'pick_up_location_id', pa.int64(), BigInteger()),
    Field('DOLocationID', 'drop_off_location_id', pa.int64(), BigInteger()),
    Field('payment_type', 'payment_type', pa.int64(), BigInteger()),
    Field('fare_amount', 'fare_amount', pa.float64(), Float()),
    Field('extra', 'extra', pa.float64(), Float()),
    Field('mta_tax', 'mta_tax', pa.float64(), Float()),
    Field('tip_amount', 'tip_amount', pa.float64(), Float()),
    Field('tolls_amount', 'tolls_amount', pa.float64(), Float()),
    Field('improvement_surcharge', 'improvement_surcharge', pa.float64(), Float()),
    Field('total_amount', 'total_amount', pa.float64(), Float()),
    Field('congestion_surcharge', 'congestion_surcharge', pa.float64(), Float())
]

SCHEMA_MAP: dict[DatasetType, list[Field]] = {
    DatasetType.GREEN: GREEN_TAXI_COLUMNS,
    DatasetType.YELLOW: YELLOW_TAXI_COLUMNS,
}