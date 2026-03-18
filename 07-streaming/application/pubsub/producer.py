import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from kafka import KafkaProducer

from application.config import AppConfig
from application.models import ride_serializer, Ride


class RideProducer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        log_every: int = 1000,
    ):
        self.topic        = topic
        self.log_every    = log_every

        self.producer = KafkaProducer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=ride_serializer,
        )


    @staticmethod
    def load_data(url: str, columns: list[str]) -> pd.DataFrame:
        return pd.read_parquet(url, columns=columns).drop_duplicates()

    @staticmethod
    def _build_ride(row: pd.Series) -> Ride:
        return Ride(
            pick_up_datetime=int(row.lpep_pickup_datetime.timestamp() * 1000),
            drop_off_datetime=int(row.lpep_dropoff_datetime.timestamp() * 1000),
            pick_up_location_id=int(row.PULocationID) if pd.notna(row.PULocationID) else 0,
            drop_off_location_id=int(row.DOLocationID) if pd.notna(row.DOLocationID) else 0,
            passenger_count=int(row.passenger_count) if pd.notna(row.passenger_count) else 0,
            trip_distance=float(row.trip_distance) if pd.notna(row.trip_distance) else 0.0,
            tip_amount=float(row.tip_amount) if pd.notna(row.tip_amount) else 0.0,
            total_amount=float(row.total_amount) if pd.notna(row.total_amount) else 0.0,
        )


    def produce(self) -> None:
        t0 = time.time()
        total = 0
        df = RideProducer.load_data(URL, COLUMNS)
        print(f"Sending {len(df)} rows to topic '{self.topic}'...")

        try:

            for _, row in df.iterrows():
                ride = self._build_ride(row)
                self.producer.send(self.topic, value=ride)

                total += 1
                if total % self.log_every == 0:
                    print(f"Produced {total} rows...")

            self.producer.flush()
        except KeyboardInterrupt:
            print(f"Stopped. Total rows produced: {total}")
        finally:
            elapsed = time.time() - t0
            print(f"Done. Sent {total} rows in {elapsed:.2f}s.")

            self.close()


    def close(self) -> None:
        self.producer.close()



if __name__ == "__main__":
    URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
    COLUMNS = [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "passenger_count",
        "trip_distance",
        "tip_amount",
        "total_amount",
    ]

    producer = RideProducer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        topic=AppConfig.KAFKA_TOPIC_NAME,
    )
    producer.produce()

