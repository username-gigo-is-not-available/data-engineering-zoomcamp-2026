CREATE OR REPLACE EXTERNAL TABLE `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.external_yellow`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://data_engineering_zoomcamp_2026_nyc_taxi_bucket/yellow_tripdata_2024-*.parquet']
);