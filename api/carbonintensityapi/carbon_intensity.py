import requests
from datetime import datetime, timedelta, timezone


class CarbonIntensity:
    def __init__(self):
        self.HEADERS = {'Accept': 'application/json'}

    @staticmethod
    def _minutes_to_iso8601_timestamp(minutes_from_now: float) -> str:
        """
        Add specified minutes to the current time and concert to ISO8601 format.
        :param minutes_from_now: Number of minutes to add to current time
        :return: ISO8601 formatted timestamp string
        """
        from datetime import datetime, timedelta, timezone

        target = datetime.now(timezone.utc) + timedelta(minutes=minutes_from_now)
        return target.strftime("%Y-%m-%dT%H:%MZ")

    @staticmethod
    def _hours_to_iso8601_timestamp(hours: float) -> str:
        """
        Add specified minutes to the current time and concert to ISO8601 format.
        :param hours: Number of hours to add to current time
        :return: ISO8601 formatted timestamp string
        """
        # Add hours to current time UTC
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=hours)

        # Format as ISO8601 with a trailing Z
        iso_str = future.strftime("%Y-%m-%dT%H:%MZ")

        return iso_str

    def getDataToday(self) -> dict:
        """
        Get Carbon Intensity data for today as JSON.
        :return: JSON data for today's Carbon Intensity.
        """
        r = requests.get(
            'https://api.carbonintensity.org.uk/intensity',
            params={},
            headers=self.HEADERS
        )
        return r.json()

    def getIntensityStatsUntil(self, hours_duration: float, hours_start: float = 0) -> dict:
        """
        Get Carbon Intensity statistics until a certain number of hours from now.
        :param hours_duration: Number of hours from now to get statistics until.
        :param hours_start: Number of hours from now to start getting statistics.
        :return: JSON data for Carbon Intensity statistics.
        """
        start_time = CarbonIntensity._hours_to_iso8601_timestamp(hours_start)
        end_time = CarbonIntensity._hours_to_iso8601_timestamp(hours_duration)
        r = requests.get(
            f'https://api.carbonintensity.org.uk/intensity/stats/{start_time}/{end_time}',
            params={},
            headers=self.HEADERS
        )
        return r.json()


if __name__ == "__main__":
    ci = CarbonIntensity()
    data = ci.getDataToday()
    print(data)
    stats = ci.getIntensityStatsUntil(24)
    print(stats)