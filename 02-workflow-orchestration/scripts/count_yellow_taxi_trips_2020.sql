select count(*) as number_of_rows
from yellow
where extract(year from pick_up_datetime) = 2020