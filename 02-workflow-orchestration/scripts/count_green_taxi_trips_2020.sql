select count(*) as number_of_rows
from green
where extract(year from pick_up_datetime) = 2020
