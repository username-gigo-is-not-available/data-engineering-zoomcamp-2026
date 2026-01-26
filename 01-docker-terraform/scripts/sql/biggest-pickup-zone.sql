select
       pz.zone,
       sum(total_amount) as total_amount
from ny_taxi.public.trips as t
join ny_taxi.public.zones as pz on pz.location_id = t.pick_up_location_id
where 1=1
and date(pick_up_datetime) = date('2025-11-18')
group by pz.zone
order by total_amount desc
limit 1

