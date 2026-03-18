import dataclasses
import datetime
import json
from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy.orm import DeclarativeBase


@dataclass
class Ride:
    pick_up_datetime: int
    drop_off_datetime: int
    pick_up_location_id: int
    drop_off_location_id: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float


def build_ride(row) -> Ride:
    return Ride(
        pick_up_datetime=row['lpep_pickup_datetime'],
        drop_off_datetime=row['lpep_dropoff_datetime'],
        pick_up_location_id=int(row['PULocationID']),
        drop_off_location_id=int(row['DOLocationID']),
        passenger_count=int(row['passenger_count']) if row['passenger_count'] else 0,
        trip_distance=float(row['trip_distance']),
        tip_amount=float(row['tip_amount']),
        total_amount=float(row['total_amount']),
    )


def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)

def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')


class Base(DeclarativeBase):
    pass


