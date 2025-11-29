import requests
from datetime import datetime, timedelta, timezone
import intensity_window


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

    def get_data_for_half_hour(self, date: str, half_hour_settlement: int) -> dict:
        """
        Get Carbon Intensity data for a specific half hour period of a certain date.
        :param date: Date in YYYY-MM-DD format.
        :param half_hour_settlement: Half hour settlement period between 1-48 (1 is the first settlement on this date)>
        :return: Carbon intensity data for this period.
        """
        # Ensure date is string in format YYYY-MM-DD
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date not string in YYYY-MM-DD format.")

        # Ensure half hour chosen is integer in interval [1, 48]
        if (not isinstance(half_hour_settlement, int) 
            or 1 > half_hour_settlement 
            or half_hour_settlement > 48
        ):
            raise ValueError("Half hour period chosen must be integer interval [1, 48]")

        r = requests.get(
            f'https://api.carbonintensity.org.uk/intensity/date/{date}/{half_hour_settlement}',
            params={},
            headers=self.HEADERS
        )

        data = r.json()
        return data['data'][0]


if __name__ == "__main__":
    ci = CarbonIntensity()
    data = ci.get_data_for_half_hour("2025-11-29", 1)
    print("Data:")
    print(data)
    print()
    print("DTO:")
    dto = intensity_window.IntensityWindow.from_json(data)
    print(dto)
    print(dto.time, dto.forecast, dto.actual, dto.index)
