from django.test import TestCase

import unittest


class Result:
    def __init__(self):
        self._errors = []

    def add_error(self, error):
        self._errors.append(error)

    def is_succesfull(self):
        return len(self._errors) == 0

    def errors(self):
        return self._errors


class Pupi:
    def enviar_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("Root element is missing.")
        return result


class Cliente:
    def __init__(self, cliente, sucursal, token):
        pass


class MyTestCase(unittest.TestCase):

    def test_01_send_a_basic_xml(self):
        client = self.example_client()
        pupi = Pupi()
        xml_to_send = self.basic_xml()
        result = pupi.enviar_xml(client, xml_to_send)
        self.assertTrue(result.is_succesfull())

    def test_02_an_empty_xml_has_an_error(self):
        client = self.example_client()
        pupi = Pupi()
        xml_to_send = self.empty_xml()
        result = pupi.enviar_xml(client, xml_to_send)
        self.assertFalse(result.is_succesfull())
        self.assertTrue(len(result.errors()) > 0)

    def example_client(self):
        client_name = "PROD-RUN"
        sucursal = "SERGI"
        token = "c949c975-5445-4bdc-8616-54a74015dc1c"
        client = Cliente(client_name, sucursal, token)
        return client

    def basic_xml(self):
        return "\
            <?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Toyota' estado='activo'>\
                    <modelo id='corolla' enLista='activo' display='Corolla' estado='activo'>\
                    </modelo>\
                </marca>\
            </marcas>\
        "

    def empty_xml(self):
        return ""


if __name__ == '__main__':
    unittest.main()


