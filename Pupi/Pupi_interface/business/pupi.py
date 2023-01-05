import xml.etree.ElementTree as ET


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        previous_brand_name = None
        previous_model_name = None
        previous_version_name = None
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        for row in rows:
            fields = row.split(',')
            
            brand_name = fields[0]
            brand_node_must_be_inserted = brand_name != previous_brand_name
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=brand_name, estado='activo')
                previous_brand_name = brand_name
                
            model_name = fields[1] if len(fields) > 1 else None
            model_node_must_be_inserted = model_name is not None and model_name != previous_model_name
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=model_name, estado='activo')
                previous_model_name = model_name
                
            version_name = fields[2] if len(fields) > 2 else None
            version_node_must_be_inserted = version_name is not None and version_name != previous_version_name
            if version_node_must_be_inserted:
                version = ET.SubElement(model, "version", display=version_name, estado='activo')
                previous_version_name = version_name

            unit_node_must_be_inserted = self._unit_data_exists(fields)
            if unit_node_must_be_inserted:
                self._create_unit_element(version, fields)

        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml

    def _unit_data_exists(self, fields):
        return len(fields) > 6

    def _create_unit_element(self, version, fields):
        ET.SubElement(version, "unidad", id=fields[6], anio=fields[3])
    