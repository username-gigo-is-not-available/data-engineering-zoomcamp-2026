SELECT window_start, total_tip
FROM tumbling_window_largest_tip
ORDER BY total_tip DESC
LIMIT 1;