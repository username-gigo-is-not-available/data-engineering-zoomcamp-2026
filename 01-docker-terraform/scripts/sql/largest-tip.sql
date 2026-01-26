select
       dz.zone,
       max(tip_amount) as largest_tip_amount
from ny_taxi.public.trips as t
join ny_taxi.public.zones as pz on pz.location_id = t.pick_up_location_id
join ny_taxi.public.zones as dz on dz.location_id = t.drop_off_location_id
where 1=1
and  pz.zone = 'East Harlem North'
and date(t.pick_up_datetime) >= date('2025-11-01')
and date(t.pick_up_datetime) <= date('2025-11-30')
group by dz.zone
order by largest_tip_amount desc
limit 1

