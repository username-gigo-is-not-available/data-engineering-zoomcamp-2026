INSERT INTO `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow`
SELECT
    CAST(VendorID AS INT64) AS vendor_id,
    CAST(tpep_pickup_datetime AS DATETIME) AS pick_up_datetime,
    CAST(tpep_dropoff_datetime AS DATETIME) AS drop_off_datetime,
    CAST(store_and_fwd_flag AS STRING) AS store_and_forward_flag,
    CAST(RatecodeID AS INT64) AS rate_code_id,
    CAST(PULocationID AS INT64) AS pick_up_location_id,
    CAST(DOLocationID AS INT64) AS drop_off_location_id,
    CAST(passenger_count AS INT64) AS passenger_count,
    CAST(trip_distance AS FLOAT64) AS trip_distance,
    CAST(fare_amount AS FLOAT64) AS fare_amount,
    CAST(extra AS FLOAT64) AS extra,
    CAST(mta_tax AS FLOAT64) AS mta_tax,
    CAST(tip_amount AS FLOAT64) AS tip_amount,
    CAST(tolls_amount AS FLOAT64) AS tolls_amount,
    CAST(improvement_surcharge AS FLOAT64) AS improvement_surcharge,
    CAST(total_amount AS FLOAT64) AS total_amount,
    CAST(payment_type AS INT64) AS payment_type,
    CAST(congestion_surcharge AS FLOAT64) AS congestion_surcharge
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.external_yellow`


