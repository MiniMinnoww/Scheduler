from datetime import datetime

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
    

    def from_json(json: str):
        time: datetime = IntensityWindow._iso8601_to_datetime(
            json['from'])

        intensity_data: dict = json['intensity']
        forecast: int = intensity_data['forecast']
        actual: int = intensity_data['actual']
        index: str = intensity_data['index']

        return IntensityWindow(time, forecast, actual, index)
