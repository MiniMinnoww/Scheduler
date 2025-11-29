class Intensity:
    """
    Represents intensity data, a component of a data point e.g. IntensityData.
    """

    def __init__(self, forecast: int, actual: int, index: str):
        this.__forecast = forecast
        this.__actual = actual
        this.__index = index

    def from_json(json: dict):
        """
        Return Intensity object parsed from json (in dict form).
        :param json: JSON dict to parse.
        """
        return Intensity(json['forecast'], json['actual'], json['index'])
