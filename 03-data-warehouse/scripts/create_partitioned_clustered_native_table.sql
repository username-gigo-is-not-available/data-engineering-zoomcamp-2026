CREATE OR REPLACE TABLE `avid-task-486715-p7.nyc_taxi_dataset.native_yellow_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT *
FROM `avid-task-486715-p7.nyc_taxi_dataset.native_yellow`;