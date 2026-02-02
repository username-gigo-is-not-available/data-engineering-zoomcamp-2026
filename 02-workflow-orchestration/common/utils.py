import calendar
from datetime import date
class DateTimeUtils:

    @classmethod
    def start_of_month(cls, year: int, month: int) -> date:
        return date(year, month, 1)

    @classmethod
    def end_of_month(cls, dt: date) -> date:
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        return date(dt.year, dt.month, last_day)

    @classmethod
    def start_of_year(cls, year: int) -> date:
        return date(year, 1, 1)

    @classmethod
    def end_of_year(cls, year) -> date:
        return date(year, 12, 31)