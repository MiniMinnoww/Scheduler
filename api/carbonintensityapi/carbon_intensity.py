import requests
from datetime import datetime, timedelta, timezone


class CarbonIntensity:
    def __init__(self):
        self.HEADERS = {'Accept': 'application/json'}

    @staticmethod
    def _hours_to_iso8601_timestamp(hours: int) -> str:
        """
        Convert current time plus 24 hours to ISO8601 format.
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
        """
        r = requests.get(
            'https://api.carbonintensity.org.uk/intensity',
            params={},
            headers=self.HEADERS
        )
        return r.json()

    def getIntensityStatsUntil(self, hours: int) -> dict:
        """
        Get Carbon Intensity statistics until a certain number of hours from now.
        """
        start_time = CarbonIntensity._hours_to_iso8601_timestamp(0)
        end_time = CarbonIntensity._hours_to_iso8601_timestamp(hours)
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