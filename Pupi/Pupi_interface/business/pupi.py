import xml.etree.ElementTree as ET


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        previous_brand_name = None
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        for row in rows:
            fields = row.split(',')
            brand_name = fields[0]
            brand_node_must_be_inserted = brand_name != previous_brand_name
            model_name = fields[1] if len(fields) > 1 else None
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=brand_name, estado='activo')
                previous_brand_name = brand_name
            model_node_must_be_inserted = model_name is not None
            if model_node_must_be_inserted:
                ET.SubElement(brand, "modelo", display=model_name, estado='activo')
        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml
    