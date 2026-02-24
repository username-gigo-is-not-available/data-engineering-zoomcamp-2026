# Module 6 Homework

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2025-11 data from the official website:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/pyspark.md)

```bash
spark-submit --version
WARNING: Using incubator modules: jdk.incubator.vector
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 4.1.1
      /_/
                        
Using Scala version 2.13.17, Java HotSpot(TM) 64-Bit Server VM, 17.0.12
Branch HEAD
Compiled by user runner on 2026-01-02T11:55:02Z
Revision c0690c763bafabd08e7079d1137fa0a769a05bae
Url https://github.com/apache/spark
Type --help for more information.
```

## Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- **25MB**
- 75MB
- 100MB

```python
@staticmethod
def average_partitioned_file_size(path: Path):
    total_bytes: float = sum(f.stat().st_size for f in Path(path).glob('**/*.parquet'))
    num_files: int = len(list(Path(path).glob('**/*.parquet')))
    logging.info(f"Total Disk Size: {total_bytes / (1024 * 1024):.2f} MB")
    logging.info(f"Average File Size per Partition: {(total_bytes / num_files) / (1024 * 1024):.2f} MB")
```

## Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

- 62,610
- 102,340
- **162,604**
- 225,768

```python
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
```

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 22.7
- 58.2
- **90.6**
- 134.5

```python
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
```

## Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- **4040**
- 8080

```python
def init_session() -> SparkSession:
    logging.info("Initializing Spark Session")
    return SparkSession.builder \
        .master("local[*]") \
        .appName("data-engineering-zoomcamp-2026-06-batch") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()
```


## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- **Governor's Island/Ellis Island/Liberty Island**
- Arden Heights
- Rikers Island
- Jamaica Bay

```python
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
```

## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw6
- Deadline: See the website


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

### Example post for LinkedIn

```
🚀 Week 6 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 6 - Batch Processing with Spark. Learned how to:

✅ Set up PySpark and create Spark sessions
✅ Read and process Parquet files at scale
✅ Repartition data for optimal performance
✅ Analyze millions of taxi trips with DataFrames
✅ Use Spark UI for monitoring jobs

Processing 4M+ taxi trips with Spark - distributed computing is powerful! 💪

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X

```
⚡ Module 6 of Data Engineering Zoomcamp done!

- Batch processing with Spark 🔥
- PySpark & DataFrames
- Parquet file optimization
- Spark UI on port 4040

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```