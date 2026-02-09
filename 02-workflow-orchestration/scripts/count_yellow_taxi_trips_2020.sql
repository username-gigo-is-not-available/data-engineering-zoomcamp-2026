select count(*)
from data_engineering_zoomcamp_2026_nyc_taxi_dataset.native_yellow
where extract(year from pick_up_datetime) = 2020