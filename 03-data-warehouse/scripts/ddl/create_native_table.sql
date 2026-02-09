CREATE TABLE IF NOT EXISTS `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow`
(
    vendor_id INT64,
    pick_up_datetime DATETIME,
    drop_off_datetime DATETIME,
    store_and_forward_flag STRING,
    rate_code_id INT64,
    pick_up_location_id INT64,
    drop_off_location_id INT64,
    passenger_count INT64,
    trip_distance FLOAT64,
    fare_amount FLOAT64,
    extra FLOAT64,
    mta_tax FLOAT64,
    tip_amount FLOAT64,
    tolls_amount FLOAT64,
    improvement_surcharge FLOAT64,
    total_amount FLOAT64,
    payment_type INT64,
    congestion_surcharge FLOAT64
);

