from django.test import TestCase

import unittest

from Pupi_interface.business import Cliente
from Pupi_interface.business.pupi import Pupi
from Pupi_interface.business.simulated_pupi import SimulatedPupi
from Pupi_interface.business.remote_pupi import RemotePupi


class PupiSendCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        super(PupiSendCatalogTest, self).setUp()
        self.pupi = RemotePupi()

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
        self.pupi = Pupi()

    def test01xxx(self):
        csv = self.example_csv_brand_audi()
        xml = self.pupi.convert_to_xml(csv)
        self.assertTrue(len(xml) > 0)

    def test02xxx(self):
        csv = self.example_csv_brand_audi()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_audi()
        self.assertEqual(expected_xml, created_xml)

    def test03xxx(self):
        csv = self.example_csv_brand_toyota()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_toyota()
        self.assertEqual(expected_xml, created_xml)

    def test04xxx(self):
        csv = self.example_csv_brand_and_model_audi()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_and_model_audi()
        self.assertEqual(expected_xml, created_xml)

    def test05xxx(self):
        csv = self.example_csv_brand_and_model_toyota()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_and_model_toyota()
        self.assertEqual(expected_xml, created_xml)

    def test06_can_convert_a_multiple_csv_line_into_xml(self):
        csv = self.example_csv_two_different_brands()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_two_different_brands()
        self.assertEqual(expected_xml, created_xml)

    def test07_can_nest_lines_with_the_same_brands(self):
        csv = self.example_csv_with_two_same_brands()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_audi()
        self.assertEqual(expected_xml, created_xml)

    def test08_xxx_same_brand_and_different_model(self):
        csv = self.example_csv_with_two_same_brand_and_different_model()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_with_two_same_brand_and_different_model()
        self.assertEqual(expected_xml, created_xml)

    def test09_xxx_brand_and_model_with_version(self):
        csv = self.example_csv_with_same_brand_and_model_with_version()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_and_version_audi()
        self.assertEqual(expected_xml, created_xml)

    def test10_xxx_same_brand_and_model_with_two_version(self):
        csv = self.example_csv_with_same_brand_and_model_with_two_version()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_and_two_version_audi()
        self.assertEqual(expected_xml, created_xml)

    def test11_xxx_same_brand_and_model_with_two_different_version(self):
        csv = self.example_csv_with_same_brand_and_model_with_two_same_version()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_and_two_same_version_audi()
        self.assertEqual(expected_xml, created_xml)

    def test12_xxx_brand_and_model_version_with_unit(self):
        csv = self.example_csv_with_brand_model_version_and_unit()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_version_and_unit()
        self.assertEqual(expected_xml, created_xml)

    def test13_xxx_brand_model_with_unit_id(self):
        csv = self.example_csv_with_brand_model_with_unit_id()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_id()
        self.assertEqual(expected_xml, created_xml)

    def test14_xxx_unit_with_image(self):
        csv = self.example_csv_with_unit_with_image()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_unit_with_image()
        self.assertEqual(expected_xml, created_xml)

    def example_csv_brand_audi(self):
        return "Audi"

    def example_csv_with_two_same_brands(self):
        return "Audi\nAudi"

    def example_xml_brand_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_brand_toyota(self):
        return "Toyota"

    def example_xml_brand_toyota(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Toyota\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_brand_and_model_audi(self):
        return "Audi,A1"

    def example_xml_brand_and_model_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_brand_and_model_toyota(self):
        return "Toyota,Etios"

    def example_csv_two_different_brands(self):
        return "Audi\nToyota"

    def example_csv_with_same_brand_and_model_with_version(self):
        return "Audi,A1,sportback"

    def example_csv_with_two_same_brand_and_different_model(self):
        return "Audi,A1\nAudi,A3"



    def example_xml_brand_model_and_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <version display=\"sportback\" estado=\"activo\">\n\
                <unidad />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_same_brand_and_model_with_two_version(self):
        return "Audi,A1,sportback\nAudi,A1,1.2"

    def example_xml_brand_model_and_two_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <version display=\"sportback\" estado=\"activo\">\n\
                <unidad />\n\
            </version>\n\
            <version display=\"1.2\" estado=\"activo\">\n\
                <unidad />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_same_brand_and_model_with_two_same_version(self):
        return "Audi,A1,sportback\nAudi,A1,sportback"

    def example_xml_brand_model_and_two_same_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <version display=\"sportback\" estado=\"activo\">\n\
                <unidad />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"
    def example_xml_brand_and_model_toyota(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Toyota\" estado=\"activo\">\n\
        <modelo display=\"Etios\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"


    def example_xml_two_different_brands(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
    <marca nombre=\"Toyota\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"



    def example_xml_with_two_same_brand_and_different_model(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" />\n\
        <modelo display=\"A3\" estado=\"activo\" />\n\
    </marca>\n\
</marcas>\
"

    def example_xml_with_two_same_brand_and_different_model(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
        <modelo display=\"A3\" estado=\"activo\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_version_and_unit(self):
        return "Audi,A1,sportback,,,,d6ac50a9-8377-4b2d-bcf8-8d50d4be9782"

    def example_xml_brand_model_version_and_unit(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <version display=\"sportback\" estado=\"activo\">\n\
                <unidad id=\"d6ac50a9-8377-4b2d-bcf8-8d50d4be9782\" />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_version_and_unit_without_id_and_year(self):
        return "Audi,A1,sportback,,,,"

    def example_xml_brand_model_version_and_unit_without_id_and_year(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <version display=\"sportback\" estado=\"activo\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_id(self):
        return "Audi,A1,,,,,d6ac50a9-8377-4b2d-bcf8-8d50d4be9782"

    def example_xml_brand_model_with_unit_id(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <unidad id=\"d6ac50a9-8377-4b2d-bcf8-8d50d4be9782\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_xml_unit_with_image(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\">\n\
            <unidad id=\"d6ac50a9-8377-4b2d-bcf8-8d50d4be9782\">\n\
                <imagenes>\n\
                    <url tipo=\"foto-agencia\">https://soybot.s3.amazonaws.com/media/paises/argentina/imagenes-whatapp/marcas/Ford/Focus/Focus.mp4</url>\n\
                </imagenes>\n\
            </unidad>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_unit_with_image(self):
        return "Audi,A1,,,,https://soybot.s3.amazonaws.com/media/paises/argentina/imagenes-whatapp/marcas/Ford/Focus/Focus.mp4,d6ac50a9-8377-4b2d-bcf8-8d50d4be9782"


if __name__ == '__main__':
    unittest.main()


