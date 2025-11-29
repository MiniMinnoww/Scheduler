import requests
from datetime import datetime, timedelta, timezone
from intensity_window import IntensityWindow


class CarbonIntensity:
    """
    Class to interact with the UK Carbon Intensity API.
    An indicative trend can be given up to 2 days ahead.
    """
    API_TIME_FORMAT: str = "%Y-%m-%dT%H:%MZ"  # ISO8601 format with 'Z' for UTC

    def __init__(self):
        self.HEADERS: dict = {'Accept': 'application/json'}

    @staticmethod
    def _datetime_to_yyyymmdd(dt: datetime) -> str:
        """
        Convert datetime object to YYYY-MM-DD string format.
        :param datetime: Datetime object to convert.
        """
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")

    @staticmethod
    def half_hour_index(dt: datetime) -> int:
        """
        Return which half-hour interval (1–48) a datetime falls into.
        :param dt: The datetime to evaluate.
        :return: int value in interval [1, 48]
        """
        # Ensure UTC or consistent timezone (important!)
        dt = dt.astimezone(timezone.utc)

        # Midnight
        midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        # Time since midnight
        diff = dt - midnight
        minutes = diff.total_seconds() // 60  # convert to minutes

        # Compute half-hour block (1–48)
        return int(minutes // 30 + 1)

    def get_data_for_half_hour(self, dt: datetime, half_hour_settlement: int) -> dict:
        """
        Get Carbon Intensity data for a specific half hour period of a certain date.
        :param date: Date in YYYY-MM-DD format.
        :param half_hour_settlement: Half hour settlement period between 1-48 (1 is the first settlement on this date)>
        :return: Carbon intensity data for this period.
        """
        date_str: str = datetime.strftime(dt, "%Y-%m-%d")

        r = requests.get(
            f'https://api.carbonintensity.org.uk/intensity/date/{date_str}/{half_hour_settlement}',
            params={},
            headers=self.HEADERS
        )

        data = r.json()
        return data['data'][0]


if __name__ == "__main__":
    ci = CarbonIntensity()
    dt: str = datetime.strptime("2025-11-30", "%Y-%m-%d")
    # half_hour_settlement = CarbonIntensity.half_hour_index(dt)
    for i in range(1, 48):
        dat = ci.get_data_for_half_hour(dt, i)
        dto = IntensityWindow.from_dict(dat)
        print(dto)
