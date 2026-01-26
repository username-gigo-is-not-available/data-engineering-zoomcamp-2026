select count(*) as number_of_trips
from ny_taxi.public.trips
where 1=1
and date(pick_up_datetime) >= date('2025-11-01')
and date(pick_up_datetime) <= date('2025-11-30')
and trip_distance <= 1

