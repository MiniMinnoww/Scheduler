import requests
from datetime import datetime, timedelta, timezone


class CarbonIntensity:
    """
    Class to interact with the UK Carbon Intensity API.
    An indicative trend can be given up to 2 days ahead.

    """
    API_TIME_FORMAT: str = "%Y-%m-%dT%H:%MZ"  # ISO8601 format with 'Z' for UTC

    def __init__(self):
        self.__HEADERS: dict = {'Accept': 'application/json'}

    @staticmethod
    def _minutes_to_iso8601_timestamp(minutes_from_now: float) -> str:
        """
        Add specified minutes to the current time and concert to ISO8601 format.
        :param minutes_from_now: Number of minutes to add to current time
        :return: ISO8601 formatted timestamp string
        """
        future = datetime.now(timezone.utc) + timedelta(minutes=minutes_from_now)
        return future.strftime(CarbonIntensity.API_TIME_FORMAT)

    @staticmethod
    def _hours_to_iso8601_timestamp(hours_from_now: float) -> str:
        """
        Add specified minutes to the current time and concert to ISO8601 format.
        :param hours_from_now: Number of hours to add to current time
        :return: ISO8601 formatted timestamp string
        """
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=hours_from_now)
        return future.strftime(CarbonIntensity.API_TIME_FORMAT)

    def getIntensityDataToday(self) -> dict:
        """
        Get Carbon Intensity data for today as JSON.
        :return: Data for today's Carbon Intensity.
        """
        r = requests.get(
            'https://api.carbonintensity.org.uk/intensity',
            params={},
            headers=self.__HEADERS
        )
        return r.json()

    def getIntensityDataForHalfHour(self, date: str, half_hour_settlement: int) -> dict:
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
            headers=self.__HEADERS
        )
        return r.json()

    def getIntensityStatsUntil(self, hours_duration: float, hours_start: float = 0) -> dict:
        """
        Get Carbon Intensity statistics until a certain number of hours from now.
        :param hours_duration: Number of hours from now to get statistics until.
        :param hours_start: Number of hours from now to start getting statistics.
        :return: Data for Carbon Intensity statistics.
        """
        start_time = CarbonIntensity._hours_to_iso8601_timestamp(hours_start)
        end_time = CarbonIntensity._hours_to_iso8601_timestamp(hours_start + hours_duration)
        r = requests.get(
            f'https://api.carbonintensity.org.uk/intensity/stats/{start_time}/{end_time}',
            params={},
            headers=self.__HEADERS
        )
        return r.json()


if __name__ == "__main__":
    ci = CarbonIntensity()
    t = ci.getIntensityDataForHalfHour("2025-11-29", 1)
    print(t)
    t = ci.getIntensityDataForHalfHour("2025-11-29", 2)
    print(t)
