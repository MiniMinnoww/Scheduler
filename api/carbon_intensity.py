import requests
from datetime import datetime, timedelta, timezone
from dto.intensity_window import IntensityWindow
from db import db

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
        :param dt: Datetime object to convert.
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
        :param dt: Date in YYYY-MM-DD format.
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
        if not data["data"]:
            return None

        return data['data'][0]

    def update_db_missing_future_forecasts(self) -> None:
        """
        Fetch and store any missing half-hour forecasts between now and 2 days' time.
        """ 
        existing_forecasts: list[IntensityWindow] = db.get_future_forecasts()
        # Normalise times to UTC and strip seconds/micros in case
        existing_times = {
            w.time.astimezone(timezone.utc).replace(second=0, microsecond=0)
            for w in existing_forecasts
        }

        now = datetime.now(timezone.utc)
        end = now + timedelta(days=2)

        # Truncate start time to half-hour boundary
        if now.minute < 30:
            start = now.replace(minute=0, second=0, microsecond=0)
        else:
            start = now.replace(minute=30, second=0, microsecond=0)

        # Walk every half-hour in this window, check which are missing
        new_windows: list[IntensityWindow] = []
        # print('already got:', existing_times)
        current = start
        
        while current <= end:
            if current not in existing_times:
                # Which settlement period (1–48) for this datetime?
                settlement = CarbonIntensity.half_hour_index(current)

                # Fetch from API for that date/period
                data = self.get_data_for_half_hour(current, settlement)

                # Convert from API dict to DTO objects
                if data:
                    window = IntensityWindow.from_dict(data)
                    new_windows.append(window)
                # print('just added:', window)

            current += timedelta(minutes=30)

        # Add missing forecasts to the db
        if new_windows:
            db.add_forecasts(new_windows)

    def get_intensity_data_48hrs(self) -> list[IntensityWindow]:
        """
        Returns list of intensity data points for the next 48hrs.
        The points each represent a half-hour window.
        """
        self.update_db_missing_future_forecasts()
        return db.get_future_forecasts()


if __name__ == "__main__":
    ci = CarbonIntensity()
    dt = datetime.strptime("2025-11-30", "%Y-%m-%d")
    #for i in range(1, 48):
        #dat = ci.get_data_for_half_hour(dt, i)
        #dto = IntensityWindow.from_json_dict(dat)
        #print(dto)
    print(db.get_future_forecasts())
    ci.update_db_missing_future_forecasts()
    print(db.get_future_forecasts())

