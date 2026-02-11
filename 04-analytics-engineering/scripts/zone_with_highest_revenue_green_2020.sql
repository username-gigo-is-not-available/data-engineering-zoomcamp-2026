SELECT pickup_zone, sum(revenue_monthly_total_amount) AS revenue
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.fct_monthly_zone_revenue`
WHERE extract(YEAR FROM revenue_month) = 2020
AND service_type = 'Green'
GROUP BY pickup_zone, extract(YEAR FROM revenue_month)
ORDER BY revenue DESC
LIMIT 1