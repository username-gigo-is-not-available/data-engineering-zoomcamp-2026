CREATE OR REPLACE TABLE `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow_partitioned_clustered`
PARTITION BY DATE(drop_off_datetime)
CLUSTER BY vendor_id
AS
SELECT *
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow`;