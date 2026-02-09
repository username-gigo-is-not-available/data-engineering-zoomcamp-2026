SELECT COUNT(DISTINCT vendor_id) FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow`
WHERE drop_off_datetime BETWEEN '2024-03-01' AND '2024-03-15';
--310.24MB
SELECT COUNT(DISTINCT vendor_id) FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow_partitioned_clustered`
WHERE drop_off_datetime BETWEEN '2024-03-01' AND '2024-03-15';
--26.84MB