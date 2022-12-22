from django.test import TestCase

import unittest

from Pupi_interface.business import Cliente
from Pupi_interface.business.simulated_pupi import SimulatedPupi
from Pupi_interface.business.remote_pupi import RemotePupi


class PupiSendCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        super(PupiSendCatalogTest, self).setUp()
        self.pupi = SimulatedPupi()

    def test_01_send_a_basic_xml(self):
        client = self.example_client()
        xml_to_send = self.basic_xml()
        result = self.pupi.send_xml(client, xml_to_send)
        self.assertTrue(result.is_succesfull())

    def test_02_an_invalid_xml_answers_a_result_with_error(self):
        client = self.example_client()
        xml_to_send = self.empty_xml()
        result = self.pupi.send_xml(client, xml_to_send)
        self.assertFalse(result.is_succesfull())
        self.assertTrue(len(result.errors()) > 0)

    def test_03_a_result_error_has_a_specific_format(self):
        client = self.example_client()
        xml_to_send = self.empty_xml()
        result = self.pupi.send_xml(client, xml_to_send)
        received_error = result.errors()[0]
        expected_error = "status code: 400\n" + \
                         "content: <errors xmlns=\"http://chat.soybot.com/catalogo/V1\"><error>Root element is " \
                         "missing.</error></errors>"
        self.assertEqual(expected_error, received_error)

    def example_client(self):
        client_name = "PROD-RUN"
        sucursal = "SERGI"
        token = "c949c975-5445-4bdc-8616-54a74015dc1c"
        client = Cliente(client_name, sucursal, token)
        return client

    def basic_xml(self):
        return "<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Toyota' estado='activo'>\
                    <modelo id='corolla' enLista='activo' display='Corolla' estado='activo'>\
                    </modelo>\
                </marca>\
            </marcas>\
        "

    def empty_xml(self):
        return ""


class PupiConvertCsvToXmlTest(unittest.TestCase):

    def setUp(self):
        super(PupiConvertCsvToXmlTest, self).setUp()
        self.pupi = SimulatedPupi()


    def test01xxx(self):
        csv = self.minimal_example_csv()
        xml = self.pupi.convert_to_xml(csv)
        self.assertTrue(len(xml) > 0)

    def test02xxx(self):
        csv = self.minimal_example_csv()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.basic_xml_audi()
        self.assertEqual(expected_xml, created_xml)

    def test03xxx(self):
        csv = self.minimal_example_csv_toyota()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.basic_xml_toyota()
        self.assertEqual(expected_xml, created_xml)

    def test04xxx(self):
        csv = self.csv_with_one_row_and_two_fields()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.xml_with_one_brand_and_one_model()
        self.assertEqual(expected_xml, created_xml)


    def basic_xml_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Audi' estado='activo'>\
                </marca>\
            </marcas>\
        "

    def minimal_example_csv(self):
        return "Audi"

    def minimal_example_csv_toyota(self):
        return "Toyota"

    def basic_xml_toyota(self):
        return "<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Toyota' estado='activo'>\
                </marca>\
            </marcas>\
        "

    def csv_with_one_row_and_two_fields(self):
        return "Audi,A1"

    def xml_with_one_brand_and_one_model(self):
        return "<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='Audi' estado='activo'>\
                    <modelo display='A1' estado='activo'>\
                    </modelo>\
                </marca>\
            </marcas>\
        "


if __name__ == '__main__':
    unittest.main()


