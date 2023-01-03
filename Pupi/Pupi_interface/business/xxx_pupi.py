from Pupi_interface.business import Result
from Pupi_interface.business.pupi import Pupi
import xml.etree.ElementTree as ET



class XXXPupi(Pupi):

    def send_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("status code: 400\n" + \
                             "content: <errors xmlns=\"http://chat.soybot.com/catalogo/V1\"><error>Root element is " \
                             "missing.</error></errors>")
        return result

    def convert_to_xml(self, csv):
        brand_name = csv
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        brand = ET.SubElement(brands, "marca", nombre=brand_name, estado='activo')
#         brand_element = f"                <marca nombre='{brand_name}' estado='activo'>\
#                 </marca>"
#         converted_xml = f"<?xml version='1.0' encoding='utf-8'?>\
#             <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
# {brand_element}\
#             </marcas>\
#         "
        tree = ET.ElementTree(brands)
        xml = ET.tostring(tree, encoding='utf-8', method='xml')
        return xml
