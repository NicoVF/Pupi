import requests

from Pupi_interface.business import Result


class RemotePupi:
    def send_xml(self, client, xml):
        url = "https://chat.soybot.com/catalogo"

        payload = xml
        headers = {
            'Content-Type': 'application/xml',
            'X-SOYBOT-TOKEN': client.token(),
            'X-SOYBOT-CLIENT': client.client_name(),
            'X-SOYBOT-POS': client.sucursal()
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = Result()
        if response.status_code not in range(200, 299):
            result.add_error("la respuesta no fue exitosa")
        return result
