from datetime import datetime, timezone
import sqlite3

class IntensityWindow:
    def __init__(self, time: datetime, forecast: int, actual: int, index: str):
        self.time: datetime = time
        self.forecast: int = forecast
        self.actual: int = actual
        self.index: str = index

    @staticmethod
    def _iso8601_to_datetime(ts: str) -> datetime:
        """
        Convert the ISO8601 timestamp format used by the API (e.g. '2025-11-29T15:30Z')
        into datetime object.
        :param ts: Time string to convert to datetime.
        """
        # Can't parse 'Z' so convert to '+00:00'
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    def is_future_forecast(self):
        return self.time > datetime.now(timezone.utc)

    @staticmethod
    def from_json_dict(data: dict):
        time: datetime = IntensityWindow._iso8601_to_datetime(
            data['from'])

        intensity_data: dict = data['intensity']
        forecast: int = intensity_data['forecast']
        actual: int = intensity_data['actual']
        index: str = intensity_data['index']

        return IntensityWindow(time, forecast, actual, index)

    @staticmethod
    def from_db_row(row: sqlite3.Row) -> "IntensityWindow":
        time = datetime.fromisoformat(row["forecast_time"])
        forecast = row["forecast_value"]
        actual = row["actual_value"]
        index = row["index_value"]
        return IntensityWindow(time, forecast, actual, index)
