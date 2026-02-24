from dataclasses import dataclass
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    LongType,
    DoubleType,
    StringType,
    TimestampType,
    DataType
)


@dataclass(frozen=True)
class Field:
    source_column_name: str
    destination_column_name: str
    data_type: DataType


GREEN_TAXI_FIELDS: list[Field] = [
    Field('VendorID', 'vendor_id', LongType()),
    Field('lpep_pickup_datetime', 'pick_up_datetime', TimestampType()),
    Field('lpep_dropoff_datetime', 'drop_off_datetime', TimestampType()),
    Field('store_and_fwd_flag', 'store_and_forward_flag', StringType()),
    Field('RatecodeID', 'rate_code_id', LongType()),
    Field('PULocationID', 'pick_up_location_id', LongType()),
    Field('DOLocationID', 'drop_off_location_id', LongType()),
    Field('passenger_count', 'passenger_count', LongType()),
    Field('trip_distance', 'trip_distance', DoubleType()),
    Field('fare_amount', 'fare_amount', DoubleType()),
    Field('extra', 'extra', DoubleType()),
    Field('mta_tax', 'mta_tax', DoubleType()),
    Field('tip_amount', 'tip_amount', DoubleType()),
    Field('tolls_amount', 'tolls_amount', DoubleType()),
    Field('ehail_fee', 'ehail_fee', DoubleType()),
    Field('improvement_surcharge', 'improvement_surcharge', DoubleType()),
    Field('total_amount', 'total_amount', DoubleType()),
    Field('payment_type', 'payment_type_id', LongType()),
    Field('trip_type', 'trip_type', LongType()),
    Field('congestion_surcharge', 'congestion_surcharge', DoubleType())
]

YELLOW_TAXI_FIELDS: list[Field] = [
    Field('VendorID', 'vendor_id', LongType()),
    Field('tpep_pickup_datetime', 'pick_up_datetime', TimestampType()),
    Field('tpep_dropoff_datetime', 'drop_off_datetime', TimestampType()),
    Field('passenger_count', 'passenger_count', LongType()),
    Field('trip_distance', 'trip_distance', DoubleType()),
    Field('RatecodeID', 'rate_code_id', LongType()),
    Field('store_and_fwd_flag', 'store_and_forward_flag', StringType()),
    Field('PULocationID', 'pick_up_location_id', LongType()),
    Field('DOLocationID', 'drop_off_location_id', LongType()),
    Field('payment_type', 'payment_type_id', LongType()),
    Field('fare_amount', 'fare_amount', DoubleType()),
    Field('extra', 'extra', DoubleType()),
    Field('mta_tax', 'mta_tax', DoubleType()),
    Field('tip_amount', 'tip_amount', DoubleType()),
    Field('tolls_amount', 'tolls_amount', DoubleType()),
    Field('improvement_surcharge', 'improvement_surcharge', DoubleType()),
    Field('total_amount', 'total_amount', DoubleType()),
    Field('congestion_surcharge', 'congestion_surcharge', DoubleType()),
    Field('Airport_fee', 'airport_fee', DoubleType()),
    Field('cbd_congestion_fee', 'cbd_congestion_fee', DoubleType()),
]

TAXI_ZONE_FIELDS: list[Field] = [
    Field('LocationID', 'location_id', LongType()),
    Field('Borough', 'borough', StringType()),
    Field('Zone', 'zone', StringType()),
    Field('service_zone', 'service_zone', StringType())
]

