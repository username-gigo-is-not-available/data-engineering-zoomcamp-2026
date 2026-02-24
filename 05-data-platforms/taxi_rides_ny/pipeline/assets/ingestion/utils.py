from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class DateTimeUtils:

    @staticmethod
    def parse_date(date: str) -> date:
        return datetime.strptime(date, "%Y-%m-%d").date()

    @staticmethod
    def generate_date_range(start_date: date, end_date: date) -> list[date]:
        months = []
        current = start_date.replace(day=1)

        while current < end_date:
            months.append(current)
            current += relativedelta(months=1)

        return months