import logging
from pathlib import Path

from pyspark.sql import SparkSession


def init_session() -> SparkSession:
    logging.info("Initializing Spark Session")
    return SparkSession.builder \
        .master("local[*]") \
        .appName("data-engineering-zoomcamp-2026-06-batch") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()

def init_directories(paths: list[Path]) -> None:
    for path in paths:
        logging.info(f"Initializing directory path: {path}")
        path.mkdir(parents=True, exist_ok=True)