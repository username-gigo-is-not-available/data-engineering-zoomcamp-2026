CREATE OR REPLACE TABLE `avid-task-486715-p7.nyc_taxi_dataset.native_yellow` AS
SELECT *
FROM `avid-task-486715-p7.nyc_taxi_dataset.external_yellow`
WHERE
  tpep_pickup_datetime >= '2024-01-01'
  AND tpep_pickup_datetime < '2024-07-01';