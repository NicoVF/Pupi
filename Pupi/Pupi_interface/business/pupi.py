import xml.etree.ElementTree as ET


class UnitForSale:
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model

    def brand(self):
        return self._brand

    def model(self):
        return self._model


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        previous_unit_for_sale = UnitForSale(brand=None, model=None)
        for row in rows:
            fields = row.split(',')

            unit_for_sale = UnitForSale(brand=fields[0], model=fields[1] if len(fields) > 1 else "")

            brand_node_must_be_inserted = unit_for_sale.brand() != previous_unit_for_sale.brand()
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=unit_for_sale.brand(), estado='activo')

            model_node_must_be_inserted = brand_node_must_be_inserted or unit_for_sale.model() != previous_unit_for_sale.model()
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=unit_for_sale.model(), estado='activo')
                last_valid_parent_for_unit_element = model

            

            unit_node_must_be_inserted = self._must_insert_unit_element(fields)
            if unit_node_must_be_inserted:
                self._create_unit_element(last_valid_parent_for_unit_element, fields)

            previous_unit_for_sale = unit_for_sale
        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml

    def _viejo_convert_to_xml(self, csv):
        rows = csv.splitlines()
        previous_brand_name = None
        previous_model_name = None
        previous_version_name = None
        last_valid_parent_for_unit_element = None
        previous_unit_element = None
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        for row in rows:
            fields = row.split(',')
            
            brand_name = fields[0]
            brand_node_must_be_inserted = brand_name != previous_brand_name
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=brand_name, estado='activo')
                previous_brand_name = brand_name
                
            model_name = fields[1] if len(fields) > 1 else ""
            model_node_must_be_inserted = brand_node_must_be_inserted or model_name != previous_model_name
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=model_name, estado='activo')
                previous_model_name = model_name
                last_valid_parent_for_unit_element = model
                
            version_name = fields[2] if len(fields) > 2 and fields[2] != "" else None
            version_node_must_be_inserted = version_name is not None and version_name != previous_version_name
            if version_node_must_be_inserted:
                version = ET.SubElement(model, "version", display=version_name, estado='activo')
                previous_version_name = version_name
                last_valid_parent_for_unit_element = version

            unit_node_must_be_inserted = self._must_insert_unit_element(fields)
            if unit_node_must_be_inserted:
                self._create_unit_element(last_valid_parent_for_unit_element, fields)

        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml

    def _unit_data_exists(self, fields):
        return len(fields) > 0

    def _create_unit_element(self, parent_node, fields):
        if len(fields) > 6:
            ET.SubElement(parent_node, "unidad", id=fields[6])
        else:
            ET.SubElement(parent_node, "unidad")

    def _must_insert_unit_element(self, fields):
        cuando_no_existe_una_unidad_falopa = True
        return cuando_no_existe_una_unidad_falopa and self._unit_data_exists(fields)


