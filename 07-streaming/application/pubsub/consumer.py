import time

from kafka import KafkaConsumer


from application.config import AppConfig
from application.models import ride_deserializer


class RideConsumer:
    def __init__(
            self,
            bootstrap_servers: str,
            topic: str,
            log_every: int = 1000,
            timeout_ms=3000,
    ):
        self.topic = topic
        self.log_every = log_every

        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[bootstrap_servers],
            auto_offset_reset="earliest",
            value_deserializer=ride_deserializer,
            consumer_timeout_ms=timeout_ms,
        )


    def consume(self) -> None:
        print(f"Listening to '{self.topic}'")
        t0 = time.time()
        total = 0
        long_trips = 0
        try:
            for message in self.consumer:
                ride = message.value

                total += 1
                if total % self.log_every == 0:
                    print(f"Consumed {total} rows...")

                if ride.trip_distance > 5:
                    long_trips += 1


        except KeyboardInterrupt:
            print(f"Stopped. Total rows consumed: {total}")
        finally:
            elapsed = time.time() - t0
            print(f"Done. Received {total} rows in {elapsed:.2f}s.")
            print(f"Trips with distance > 5.0 km: {long_trips}")
            self.close()

    def close(self) -> None:
        self.consumer.close()


if __name__ == "__main__":
    consumer = RideConsumer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        topic=AppConfig.KAFKA_TOPIC_NAME,
    )
    consumer.consume()
