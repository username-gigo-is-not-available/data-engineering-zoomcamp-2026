SELECT COUNT(DISTINCT VendorID) FROM `avid-task-486715-p7.nyc_taxi_dataset.native_yellow`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
--310.24MB
SELECT COUNT(DISTINCT VendorID) FROM `avid-task-486715-p7.nyc_taxi_dataset.native_yellow_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
--26.84MB
