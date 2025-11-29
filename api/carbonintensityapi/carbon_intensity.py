import requests

class CarbonIntensity:
    def __init__(self):
        self.HEADERS = {'Accept': 'application/json'}

    """
    Get Carbon Intensity data for today.
    """
    def getDataToday(self):
        r = requests.get(
            'https://api.carbonintensity.org.uk/intensity',
            params={},
            headers=self.HEADERS
        )
        return r.json()
