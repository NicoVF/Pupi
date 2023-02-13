import unittest
from unittest import skip

from Pupi_interface.business import Cliente
from Pupi_interface.business.pupi import Pupi, UnitForSale
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

    def test15_xxx_brand_model_with_unit_year(self):
        csv = self.example_csv_with_brand_model_with_unit_year()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_year()
        self.assertEqual(expected_xml, created_xml)

    def test16_xxx_brand_model_with_unit_price(self):
        csv = self.example_csv_with_brand_model_with_unit_price()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_price()
        self.assertEqual(expected_xml, created_xml)

    def test17_xxx_brand_model_with_unit_kilometers(self):
        csv = self.example_csv_with_brand_model_with_unit_kilometers()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_kilometers()
        self.assertEqual(expected_xml, created_xml)

    def test18_xxx_brand_model_with_unit_currency(self):
        csv = self.example_csv_with_brand_model_with_unit_currency()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_currency()
        self.assertEqual(expected_xml, created_xml)

    def test19_xxx_brand_model_with_unit_zone(self):
        csv = self.example_csv_with_brand_model_with_unit_zone()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_zone()
        self.assertEqual(expected_xml, created_xml)

    def test20_xxx_brand_model_with_unit_latitud(self):
        csv = self.example_csv_with_brand_model_with_unit_latitud()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_latitud()
        self.assertEqual(expected_xml, created_xml)

    def test21_xxx_brand_model_with_unit_longitud(self):
        csv = self.example_csv_with_brand_model_with_unit_longitud()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_longitud()
        self.assertEqual(expected_xml, created_xml)

    def test22_xxx_brand_model_with_unit_provider(self):
        csv = self.example_csv_with_brand_model_with_unit_provider()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_provider()
        self.assertEqual(expected_xml, created_xml)

    def test23_xxx_brand_model_with_unit_provider_of_providers(self):
        csv = self.example_csv_with_brand_model_with_unit_provider_of_providers()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_provider_of_providers()
        self.assertEqual(expected_xml, created_xml)

    def test24_xxx_brand_model_with_unit_sales_type(self):
        csv = self.example_csv_with_brand_model_with_unit_sales_type()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_brand_model_with_unit_sales_type()
        self.assertEqual(expected_xml, created_xml)

    def test25_same_version_but_different_model_must_insert_anyway(self):
        csv = self.csv_con_same_version_but_different_model_must_insert_anyway()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.xml_correcto_para_same_version_but_different_model_must_insert_anyway()
        self.assertEqual(expected_xml, created_xml)

    def example_csv_brand_audi(self):
        return "audi"

    def example_csv_with_two_same_brands(self):
        return "Audi\nAudi"

    def example_xml_brand_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\" enLista=\"activo\" id=\"\">\n\
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
        <modelo display=\"\" estado=\"activo\" enLista=\"activo\" id=\"\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_brand_and_model_audi(self):
        return "aUdi,a1"

    def example_xml_brand_and_model_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
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
        return "Audi,A1,Sportback"

    def example_csv_with_two_same_brand_and_different_model(self):
        return "Audi,A1\nAudi,A3"



    def example_xml_brand_model_and_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <version display=\"Sportback\" estado=\"activo\" enLista=\"activo\" id=\"Sportback\">\n\
                <unidad />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_same_brand_and_model_with_two_version(self):
        return "Audi,A1,1.2\nAudi,A1,Sportback"

    def example_xml_brand_model_and_two_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <version display=\"1.2\" estado=\"activo\" enLista=\"activo\" id=\"1.2\">\n\
                <unidad />\n\
            </version>\n\
            <version display=\"Sportback\" estado=\"activo\" enLista=\"activo\" id=\"Sportback\">\n\
                <unidad />\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_same_brand_and_model_with_two_same_version(self):
        return "Audi,A1,Sportback\nAudi,A1,Sportback"

    def example_xml_brand_model_and_two_same_version_audi(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <version display=\"Sportback\" estado=\"activo\" enLista=\"activo\" id=\"Sportback\">\n\
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
        <modelo display=\"Etios\" estado=\"activo\" enLista=\"activo\" id=\"etios\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"


    def example_xml_two_different_brands(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\" enLista=\"activo\" id=\"\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
    <marca nombre=\"Toyota\" estado=\"activo\">\n\
        <modelo display=\"\" estado=\"activo\" enLista=\"activo\" id=\"\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"



    def example_xml_with_two_same_brand_and_different_model(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad />\n\
        </modelo>\n\
        <modelo display=\"A3\" estado=\"activo\" enLista=\"activo\" id=\"a3\">\n\
            <unidad />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_version_and_unit(self):
        return "Audi,A1,Sportback,,,,d6ac50a9-8377-4b2d-bcf8-8d50d4be9782"

    def example_xml_brand_model_version_and_unit(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <version display=\"Sportback\" estado=\"activo\" enLista=\"activo\" id=\"Sportback\">\n\
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
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <version display=\"Sportback\" estado=\"activo\" enLista=\"activo\"  id=\"sportback\"/>\n\
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
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad id=\"d6ac50a9-8377-4b2d-bcf8-8d50d4be9782\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"


    def example_xml_unit_with_image(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
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

    def example_csv_with_brand_model_with_unit_year(self):
        return "Audi,A1,,2013,,,d6ac50a9-8377-4b2d-bcf8-8d50d4be9782"

    def example_xml_brand_model_with_unit_year(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad id=\"d6ac50a9-8377-4b2d-bcf8-8d50d4be9782\" anio=\"2013\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_price(self):
        return "Audi,A1,,,1500000,,"

    def example_xml_brand_model_with_unit_price(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad precio=\"1500000\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_currency(self):
        return "Audi,A1,,,,,,,USD"

    def example_xml_brand_model_with_unit_currency(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad tipoCambio=\"USD\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"
    def example_csv_with_brand_model_with_unit_zone(self):
        return "Audi,A1,,,,,,,,\"Acassuso, Av Libertador, 14745\""

    def example_xml_brand_model_with_unit_zone(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad zona=\"Acassuso, Av Libertador, 14745\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_latitud(self):
        return "Audi,A1,,,,,,,,,\"-34,5951836\""

    def example_xml_brand_model_with_unit_latitud(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad lat=\"-34.5951836\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_longitud(self):
        return "Audi,A1,,,,,,,,,,\"-58,3745734\""

    def example_xml_brand_model_with_unit_longitud(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad long=\"-58.3745734\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_kilometers(self):
        return "Audi,A1,,,,,,58000,,"

    def example_xml_brand_model_with_unit_kilometers(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad kilometros=\"58000\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_provider(self):
        return "Audi,A1,,,,,,,,,,,Munafo Virtual"

    def example_xml_brand_model_with_unit_provider(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad cliente=\"Munafo Virtual\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_provider_of_providers(self):
        return "Audi,A1,,,,,,,,,,,,DeConcesionarias"

    def example_xml_brand_model_with_unit_provider_of_providers(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad proveedorProveedores=\"DeConcesionarias\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def example_csv_with_brand_model_with_unit_sales_type(self):
        return "Audi,A1,,,,,,,,,,,,,Usado"

    def example_xml_brand_model_with_unit_sales_type(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad tipoVenta=\"Usado\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"

    def csv_con_same_version_but_different_model_must_insert_anyway(self):
        return """""nissan,March,1.6 SENSE PURE DRIVE,2018,3100000,https://api.deconcesionarias.com.ar/api/files/e5e06f5f-63a6-4486-975a-ee228dc74e1f/?e5e06f5f-63a6-4486-975a-ee228dc74e1f.jpg,3e9c3edf-ecc7-4167-be8a-6f02b2abcbd5,65000,ARS,"SAN LUIS, Av. del Fundador esq, Las voces del Chorrillero,","-33,2941809","-66,2956203",ExpoUsados,DeConcesionarias,Usado
nissan,note,1.6 SENSE PURE DRIVE,2018,4290000,https://api.deconcesionarias.com.ar/api/files/55af7001-58e5-4228-b1bb-888ff9106b18/?55af7001-58e5-4228-b1bb-888ff9106b18.jpg,7fd4db2a-eb99-46d8-8ac3-01dcd66dd436,70000,ARS,"PILAR, Las Camelias, 3190","-34,4383348","-58,7918752",Autonorte Pilar S.A,DeConcesionarias,Usado
"""""

    def xml_correcto_para_same_version_but_different_model_must_insert_anyway(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Nissan\" estado=\"activo\">\n\
        <modelo display=\"March\" estado=\"activo\" enLista=\"activo\" id=\"march\">\n\
            <version display=\"1.6 Sense Pure Drive\" estado=\"activo\" enLista=\"activo\" id=\"1.6 Sense Pure Drive\">\n\
                <unidad id=\"3e9c3edf-ecc7-4167-be8a-6f02b2abcbd5\" kilometros=\"65000\" anio=\"2018\" precio=\"3100000\" tipoCambio=\"ARS\" zona=\"San Luis, Av. Del Fundador Esq, Las Voces Del Chorrillero,\" lat=\"-33.2941809\" long=\"-66.2956203\" cliente=\"ExpoUsados\" proveedorProveedores=\"DeConcesionarias\" tipoVenta=\"Usado\">\n\
                    <imagenes>\n\
                        <url tipo=\"foto-agencia\">https://api.deconcesionarias.com.ar/api/files/e5e06f5f-63a6-4486-975a-ee228dc74e1f/?e5e06f5f-63a6-4486-975a-ee228dc74e1f.jpg</url>\n\
                    </imagenes>\n\
                </unidad>\n\
            </version>\n\
        </modelo>\n\
        <modelo display=\"Note\" estado=\"activo\" enLista=\"activo\" id=\"note\">\n\
            <version display=\"1.6 Sense Pure Drive\" estado=\"activo\" enLista=\"activo\" id=\"1.6 Sense Pure Drive\">\n\
                <unidad id=\"7fd4db2a-eb99-46d8-8ac3-01dcd66dd436\" kilometros=\"70000\" anio=\"2018\" precio=\"4290000\" tipoCambio=\"ARS\" zona=\"Pilar, Las Camelias, 3190\" lat=\"-34.4383348\" long=\"-58.7918752\" cliente=\"Autonorte Pilar S.A\" proveedorProveedores=\"DeConcesionarias\" tipoVenta=\"Usado\">\n\
                    <imagenes>\n\
                        <url tipo=\"foto-agencia\">https://api.deconcesionarias.com.ar/api/files/55af7001-58e5-4228-b1bb-888ff9106b18/?55af7001-58e5-4228-b1bb-888ff9106b18.jpg</url>\n\
                    </imagenes>\n\
                </unidad>\n\
            </version>\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"


if __name__ == '__main__':
    unittest.main()


class PupiNormalizationWhenConvertingCsvToXmlTest(unittest.TestCase):

    def setUp(self):
        super(PupiNormalizationWhenConvertingCsvToXmlTest, self).setUp()
        self.pupi = Pupi()

    def test01_ignore_case_in_brand_name(self):
        csv = self.example_csv_with_two_brands_with_different_case()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_two_brands_with_different_case()
        self.assertEqual(expected_csv, normalized_csv)

    def test02_ignore_case_in_model_name(self):
        csv = self.example_csv_with_two_model_with_different_case()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_two_model_with_different_case()
        self.assertEqual(expected_csv, normalized_csv)

    def test03_replace_comma_with_dot_in_lat_and_long(self):
        csv = self.example_csv_with_model_with_lat_and_long()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model_with_lat_and_long()
        self.assertEqual(expected_csv, normalized_csv)

    def test04_capitalize_each_word_in_version(self):
        csv = self.example_csv_with_long_version_name()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_long_version_name()
        self.assertEqual(expected_csv, normalized_csv)

    def test05_capitalize_each_word_in_zone(self):
        csv = self.example_csv_with_model_with_zone()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model_with_zone()
        self.assertEqual(expected_csv, normalized_csv)

    def test06_capitalize_each_word_in_brand(self):
        csv = self.example_csv_with_model()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_model()
        self.assertEqual(expected_csv, normalized_csv)

    def test07_capitalize_each_word_in_brand_and_model(self):
        csv = self.example_csv_with_brand_and_model()
        normalized_csv = self.pupi.normalize_csv(csv)
        expected_csv = self.example_normalized_csv_with_brand_and_model()
        self.assertEqual(expected_csv, normalized_csv)

    def example_csv_with_two_brands_with_different_case(self):
        return "AUDI\naudi"

    def example_normalized_csv_with_two_brands_with_different_case(self):
        return """"Audi"\n"Audi\""""

    def example_csv_with_two_model_with_different_case(self):
        return "Toyota,COROLLA\ntoyota,coRolla"

    def example_normalized_csv_with_two_model_with_different_case(self):
        return """"Toyota","Corolla"\n"Toyota","Corolla\""""

    def example_csv_with_model_with_lat_and_long(self):
        return "Audi,A1,,,,,,,,,\"-34,3745734\",\"-58,3745734\""

    def example_normalized_csv_with_model_with_lat_and_long(self):
        return """"Audi","A1","","","","","","","","","-34.3745734","-58.3745734\""""

    def example_csv_with_long_version_name(self):
        return "Toyota,COROLLA,1.6 SENSE DRIVE AUTOMATIC\ntoyota,coRolla,1.6 sense drive automatic"

    def example_normalized_csv_with_long_version_name(self):
        return """"Toyota","Corolla","1.6 Sense Drive Automatic"\n"Toyota","Corolla","1.6 Sense Drive Automatic\""""

    def example_csv_with_model_with_zone(self):
        return "Audi,A1,,,,,,,,\"SAN LUIS, Av. del Fundador esq, Las voces del Chorrillero,\""

    def example_normalized_csv_with_model_with_zone(self):
        return """"Audi","A1","","","","","","","","San Luis, Av. Del Fundador Esq, Las Voces Del Chorrillero,\""""

    def example_csv_with_model(self):
        return "Audi,a1 sport"

    def example_normalized_csv_with_model(self):
        return """"Audi","A1 Sport\""""

    def example_csv_with_brand_and_model(self):
        return "Alfa romeo"

    def example_normalized_csv_with_brand_and_model(self):
        return """"Alfa Romeo\""""

    def example_csv_with_brands_not_sorted(self):
        return "Chevrolet\nAudi"

    def example_normalized_csv_with_brands_sorted(self):
        return """"Audi"\n"Chevrolet\""""

    def example_csv_with_models_not_sorted(self):
        return "Audi,B250\nAudi,A1"

    def example_normalized_csv_with_models_sorted(self):
        return """"Audi","A1"\n"Audi","B250\""""

    def example_csv_with_models_not_sorted_and_different_brand(self):
        return "Chevrolet,S10\nAudi,A1"

    def example_normalized_csv_with_models_sorted_and_different_brand(self):
        return """"Audi","A1"\n"Chevrolet","S10\""""

    def example_csv_with_versions_not_sorted(self):
        return "Audi,A1,Bt. Tetronic\nAudi,A1,1.4T Turbo"

    def example_normalized_csv_with_versions_sorted(self):
        return """"Audi","A1","1.4T Turbo"\n"Audi","A1","Bt. Tetronic\""""

    def example_csv_with_same_units_not_sorted(self):
        return "Audi,A1,,,1500000\nAudi,A1,,,2500000"

    def example_normalized_csv_with_same_unit_sorted(self):
        return """"Audi","A1","","","2500000"\n"Audi","A1","","","1500000\""""

    def example_csv_with_same_units_by_year(self):
        return "Audi,A1,,2019\nAudi,A1,,2022"

    def example_normalized_csv_with_same_unit_by_year_sorted(self):
        return """"Audi","A1","","2022"\n"Audi","A1","","2019\""""

    def example_csv_with_same_units_by_year_with_only_one_year(self):
        return "Audi,A1,,\nAudi,A1,,2022"

    def example_normalized_csv_with_same_unit_by_year_sorted_with_only_one_year(self):
        return """"Audi","A1","","2022"\n"Audi","A1","","\""""


class PupiSortUnitForSaleTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.unit_audi = UnitForSale.create_unit_from(["Audi"])
        self.unit_audi_A1 = UnitForSale.create_unit_from(["Audi", "A1"])
        self.unit_audi_A3 = UnitForSale.create_unit_from(["Audi", "A3"])
        self.unit_fiat = UnitForSale.create_unit_from(["Fiat"])
        self.unit_fiat_palio_nafta = UnitForSale.create_unit_from(["Fiat", "Palio", "Nafta"])
        self.unit_fiat_palio_gnc = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC"])
        self.unit_fiat_palio_gnc_precio150 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "150"])
        self.unit_fiat_palio_gnc_precio250 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "250"])
        self.unit_fiat_palio_gnc_precio350 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "350"])
        self.unit_fiat_palio_gnc_anio2015 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015"])
        self.unit_fiat_palio_gnc_anio2018 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018"])
        self.unit_fiat_palio_gnc_anio2015_precio150 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015", "150"])
        self.unit_fiat_palio_gnc_anio2015_precio350 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015", "350"])
        self.unit_fiat_palio_gnc_anio2018_precio150 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018", "150"])
        self.unit_fiat_palio_gnc_anio2018_precio250 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018", "250"])
        self.unit_fiat_palio_gnc_anio2018_precio250_2 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018", "250"])
        self.unit_fiat_palio_gnc_anio2017_precio750 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2017", "750"])
        super(PupiSortUnitForSaleTest, self).setUp()
        self.pupi = Pupi()

    def test01_sorts_brands(self):
        units = self.example_units_with_brands_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_brands_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test02_sorts_model_with_same_brand(self):
        units = self.example_units_with_models_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_models_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test03_sorts_version_with_same_model(self):
        units = self.example_units_with_versions_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_versions_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test04_sorts_highest_price_first_within_same_version(self):
        units = self.example_units_with_price_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test05_sorts_highest_year_with_same_price(self):
        units = self.example_units_with_year_not_sorted()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_with_year_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test06_sorts_units_by_year_with_only_one_year(self):
        units = self.example_units_by_year_with_only_one_year()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test07_sorts_units_by_year_with_different_year_and_same_price(self):
        units = self.example_units_by_year_with_different_year_and_same_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_and_same_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test08_sorts_units_by_year_with_different_year_and_different_price(self):
        units = self.example_units_by_year_with_different_year_and_different_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_units_by_year_with_only_one_year_and_different_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def test09_sorts_many_units_by_year_with_different_year_and_different_price(self):
        units = self.example_many_units_by_year_with_different_year_and_different_price()
        sorted_units = self.pupi._sort_units_for_sale(units)
        expected_units = self.example_many_units_by_year_with_only_one_year_and_different_price_sorted()
        self.assertEqual(expected_units, sorted_units)

    def example_units_with_brands_not_sorted(self):
        return [self.unit_fiat,
                self.unit_audi]

    def example_units_with_brands_sorted(self):
        return [self.unit_audi,
                self.unit_fiat]

    def example_units_with_models_not_sorted(self):
        return [self.unit_audi_A3,
                self.unit_audi_A1]

    def example_units_with_models_sorted(self):
        return [self.unit_audi_A1,
                self.unit_audi_A3]

    def example_units_with_versions_not_sorted(self):
        return [self.unit_fiat_palio_nafta,
                self.unit_fiat_palio_gnc]

    def example_units_with_versions_sorted(self):
        return [self.unit_fiat_palio_gnc,
                self.unit_fiat_palio_nafta]

    def example_units_with_price_not_sorted(self):
        return [self.unit_fiat_palio_gnc_precio250,
                self.unit_fiat_palio_gnc_precio150]

    def example_units_with_price_sorted(self):
        return [self.unit_fiat_palio_gnc_precio150,
                self.unit_fiat_palio_gnc_precio250]

    def example_units_with_year_not_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2018,
                self.unit_fiat_palio_gnc_anio2015]

    def example_units_with_year_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015,
                self.unit_fiat_palio_gnc_anio2018]

    def example_units_by_year_with_only_one_year(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_units_by_year_with_only_one_year_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250]

    def example_units_by_year_with_different_year_and_same_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2015_precio150]

    def example_units_by_year_with_only_one_year_and_same_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_units_by_year_with_different_year_and_different_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2017_precio750]

    def example_units_by_year_with_only_one_year_and_different_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio150]

    def example_many_units_by_year_with_different_year_and_different_price(self):
        return [self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio250_2,
                self.unit_fiat_palio_gnc_anio2015_precio350]

    def example_many_units_by_year_with_only_one_year_and_different_price_sorted(self):
        return [self.unit_fiat_palio_gnc_anio2015_precio150,
                self.unit_fiat_palio_gnc_anio2015_precio350,
                self.unit_fiat_palio_gnc_anio2017_precio750,
                self.unit_fiat_palio_gnc_anio2018_precio150,
                self.unit_fiat_palio_gnc_anio2018_precio250,
                self.unit_fiat_palio_gnc_anio2018_precio250_2]


class PupiForSaleOrderTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.unit_audi = UnitForSale.create_unit_from(["Audi"])
        self.unit_audi_A1 = UnitForSale.create_unit_from(["Audi", "A1"])
        self.unit_audi_A3 = UnitForSale.create_unit_from(["Audi", "A3"])
        self.unit_fiat = UnitForSale.create_unit_from(["Fiat"])
        self.unit_fiat_palio_nafta = UnitForSale.create_unit_from(["Fiat", "Palio", "Nafta"])
        self.unit_fiat_palio_gnc = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC"])
        self.unit_fiat_palio_gnc_precio150 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "150"])
        self.unit_fiat_palio_gnc_precio1000 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "1000"])
        self.unit_fiat_palio_gnc_precio250 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "", "250"])
        self.unit_fiat_palio_gnc_anio2015 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2015"])
        self.unit_fiat_palio_gnc_anio2018 = UnitForSale.create_unit_from(["Fiat", "Palio", "GNC", "2018"])
        super(PupiForSaleOrderTest, self).setUp()
        self.pupi = Pupi()

    def test01_same_units_with_brand(self):
        self.assertEqual(self.unit_audi, self.unit_audi)

    def test02_different_units_with_model(self):
        self.assertNotEqual(self.unit_audi_A1, self.unit_audi_A3)

    def test03_first_unit_less_than_second_unit_with_model(self):
        self.assertLess(self.unit_audi_A1, self.unit_audi_A3)

    def test04_first_unit_great_than_second_unit_with_model(self):
        self.assertGreater(self.unit_audi_A3, self.unit_audi_A1)

    def test05_same_units_with_version(self):
        self.assertEqual(self.unit_fiat_palio_gnc, self.unit_fiat_palio_gnc)

    def test06_different_units_with_brand(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc, self.unit_fiat_palio_nafta)

    def test07_first_unit_less_than_second_unit_with_version(self):
        self.assertLess(self.unit_fiat_palio_gnc, self.unit_fiat_palio_nafta)

    def test08_first_unit_great_than_second_unit_with_version(self):
        self.assertGreater(self.unit_fiat_palio_nafta, self.unit_fiat_palio_gnc)

    def test09_same_units_with_price(self):
        self.assertEqual(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio150)

    def test10_different_units_with_price(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio250)

    def test11_first_unit_less_than_second_unit_with_price(self):
        self.assertLess(self.unit_fiat_palio_gnc_precio150, self.unit_fiat_palio_gnc_precio250)

    def test12_first_unit_great_than_second_unit_with_price(self):
        self.assertGreater(self.unit_fiat_palio_gnc_precio250, self.unit_fiat_palio_gnc_precio150)

    def test13_same_units_with_year(self):
        self.assertEqual(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2015)

    def test14_different_units_with_year(self):
        self.assertNotEqual(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2018)

    def test15_first_unit_less_than_second_unit_with_year(self):
        self.assertLess(self.unit_fiat_palio_gnc_anio2015, self.unit_fiat_palio_gnc_anio2018)

    def test16_first_unit_great_than_second_unit_with_year(self):
        self.assertGreater(self.unit_fiat_palio_gnc_anio2018, self.unit_fiat_palio_gnc_anio2015)
    def test17_lexicographic_order_of_price_doesnt_matter(self):
        self.assertLess(self.unit_fiat_palio_gnc_precio250, self.unit_fiat_palio_gnc_precio1000)
