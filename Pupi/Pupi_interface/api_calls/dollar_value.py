import requests


class DollarValue:

    def __init__(self):
        url = "https://api.bluelytics.com.ar/v2/latest"
        self._dollar_value = None

        payload = {}
        try:
            response = requests.request("GET", url, data=payload)
            self._dollar_value = int(response.json().get('blue').get('value_avg'))
        except:
            raise ValueError("No pudimos obtener la cotizacion online. Por favor ingresela manualmente")

    def dollar_value(self):
        return self._dollar_value
