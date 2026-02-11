SELECT
    sum(total_monthly_trips)
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.fct_monthly_zone_revenue`
WHERE EXTRACT(YEAR FROM revenue_month) = 2019
  AND EXTRACT(MONTH FROM revenue_month) = 10
  AND service_type = 'Green'
