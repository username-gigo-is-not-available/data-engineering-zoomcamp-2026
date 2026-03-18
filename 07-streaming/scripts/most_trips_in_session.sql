SELECT PULocationID, num_trips
FROM session_window_longest_streak
ORDER BY num_trips DESC
LIMIT 1;