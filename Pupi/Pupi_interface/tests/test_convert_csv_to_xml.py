import unittest

from Pupi_interface.business.pupi import Pupi


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

    def test25_we_write_the_client_ID_in_the_xml(self):
        csv = self.example_csv_with_client_id()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.example_xml_with_client_id()
        self.assertEqual(expected_xml, created_xml)

    def test26_same_version_but_different_model_must_insert_anyway(self):
        csv = self.csv_con_same_version_but_different_model_must_insert_anyway()
        created_xml = self.pupi.convert_to_xml(csv)
        expected_xml = self.xml_correcto_para_same_version_but_different_model_must_insert_anyway()
        self.assertEqual(expected_xml, created_xml)

    def example_csv_brand_audi(self):
        return "Audi"

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
        return "Audi,A1"

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
        return "Audi,A1,,,1500000,,,,,,,,,,,,1500000"

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
        return "Audi,A1,,,,,,,,,\"-34.5951836\""

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
        return "Audi,A1,,,,,,,,,,\"-58.3745734\""

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
        return """""Nissan,March,1.6 Sense Pure Drive,2018,3100000,https://api.deconcesionarias.com.ar/api/files/e5e06f5f-63a6-4486-975a-ee228dc74e1f/?e5e06f5f-63a6-4486-975a-ee228dc74e1f.jpg,3e9c3edf-ecc7-4167-be8a-6f02b2abcbd5,65000,ARS,"San Luis, Av. Del Fundador Esq, Las Voces Del Chorrillero,","-33.2941809","-66.2956203",ExpoUsados,DeConcesionarias,Usado,,3100000
Nissan,Note,1.6 Sense Pure Drive,2018,4290000,https://api.deconcesionarias.com.ar/api/files/55af7001-58e5-4228-b1bb-888ff9106b18/?55af7001-58e5-4228-b1bb-888ff9106b18.jpg,7fd4db2a-eb99-46d8-8ac3-01dcd66dd436,70000,ARS,"Pilar, Las Camelias, 3190","-34.4383348","-58.7918752",Autonorte Pilar S.A,DeConcesionarias,Usado,,4290000
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

    def example_csv_with_client_id(self):
        return "Audi,A1,,,,,,,,,,,,,,b913a258-6ab0-406b-bae7-e4f8e5d0e6ewqr"

    def example_xml_with_client_id(self):
        return "<?xml version='1.0' encoding='utf-8'?>\n\
<marcas xmlns=\"http://chat.soybot.com/catalogo/V1\">\n\
    <marca nombre=\"Audi\" estado=\"activo\">\n\
        <modelo display=\"A1\" estado=\"activo\" enLista=\"activo\" id=\"a1\">\n\
            <unidad idDeCliente=\"b913a258-6ab0-406b-bae7-e4f8e5d0e6ewqr\" />\n\
        </modelo>\n\
    </marca>\n\
</marcas>\
"
