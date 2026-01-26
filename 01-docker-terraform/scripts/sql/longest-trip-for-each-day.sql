select date(pick_up_datetime) as pickup_date,
       max(trip_distance) as max_distance
from ny_taxi.public.trips
where 1=1
and date(pick_up_datetime) >= date('2025-11-01')
and date(pick_up_datetime) <= date('2025-11-30')
and trip_distance < 100
group by date(pick_up_datetime)
order by max_distance desc
limit 1


