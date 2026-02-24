from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def count_trips_for_date(df: DataFrame, dt: date) -> int:
    return (
        df
        .select(
            "vendor_id",
            "pick_up_datetime",
            "drop_off_datetime",
            "rate_code_id",
            "pick_up_location_id",
            "drop_off_location_id",
        )
        .filter(
            (F.year(F.col("pick_up_datetime")) == dt.year) &
            (F.month(F.col("pick_up_datetime")) == dt.month) &
            (F.day(F.col("drop_off_datetime")) == dt.day)
        )
        .distinct()
        .count()
    )


def longest_trip_duration(df: DataFrame) -> float:
    df_duration: DataFrame = (
        df
        .withColumn(
            "duration_hours",
            (F.col("drop_off_datetime").cast("long") - F.col("pick_up_datetime").cast("long")) / 3600
        )
    )

    return (
        df_duration.
        select(
            F.max("duration_hours")
            .alias("max_duration_hours")
        )
        .first()
        .max_duration_hours
    )


def frequency_by_location_id(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("pick_up_location_id")
        .agg(F.count("pick_up_location_id").alias("total_pick_ups"))
    )


def least_frequent_pick_up_zone(df_trips: DataFrame, df_zones: DataFrame) -> DataFrame:
    df_trips: DataFrame = frequency_by_location_id(df_trips)
    return (
        df_zones
        .join(
            other=df_trips,
            on=df_zones.location_id == df_trips.pick_up_location_id,
            how="left"
        )
        .fillna(0, subset=["total_pick_ups"])
        .select("zone", "total_pick_ups")
        .distinct()
        .sort(
            F.asc("total_pick_ups"), F.asc("zone")
        )
        .first()
        .zone
    )
