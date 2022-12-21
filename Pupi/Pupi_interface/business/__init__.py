class Result:
    def __init__(self):
        self._errors = []

    def add_error(self, error):
        self._errors.append(error)

    def is_succesfull(self):
        return len(self._errors) == 0

    def errors(self):
        return self._errors


class SimulatedPupi:
    def send_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("status code: 400\n" + \
                             "content: <errors xmlns=\"http://chat.soybot.com/catalogo/V1\"><error>Root element is " \
                             "missing.</error></errors>")
        return result

    def convert_to_xml(self, csv):
        return "<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Audi' estado='activo'>\
                </marca>\
            </marcas>\
        "


class Cliente:
    def __init__(self, cliente, sucursal, token):
        self._client_name = cliente
        self._sucursal = sucursal
        self._token = token

    def client_name(self):
        return self._client_name

    def sucursal(self):
        return self._sucursal

    def token(self):
        return self._token
