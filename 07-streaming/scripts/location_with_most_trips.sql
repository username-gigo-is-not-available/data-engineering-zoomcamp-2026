SELECT PULocationID, num_trips
FROM tumbling_window_pickup_location
ORDER BY num_trips DESC
LIMIT 1;