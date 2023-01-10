import xml.etree.ElementTree as ET


class UnitForSale:
    def __init__(self, brand, model, version, id):
        self._brand = brand
        self._model = model
        self._version = version
        self._id = id

    def __eq__(self, other):
        return self._brand == other.brand() and self._model == other.model()

    def brand(self):
        return self._brand

    def model(self):
        return self._model

    def version(self):
        return self._version

    def id(self):
        return self._id

    def has_id(self):
        return self._id

    def has_valid_brand(self):
        return self._brand is not None


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        previous_unit_for_sale = UnitForSale(brand=None, model="", version=None, id=None)
        for row in rows:
            fields = row.split(',')

            unit_for_sale = UnitForSale(brand=fields[0], model=fields[1] if len(fields) > 1 else "",
                                        version=fields[2] if len(fields) > 2 and fields[2] != "" else None,
                                        id=fields[6] if len(fields) > 6 else None)

            brand_node_must_be_inserted = unit_for_sale.brand() != previous_unit_for_sale.brand()
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=unit_for_sale.brand(), estado='activo')

            model_node_must_be_inserted = brand_node_must_be_inserted or unit_for_sale.model() != previous_unit_for_sale.model()
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=unit_for_sale.model(), estado='activo')
                last_valid_parent_for_unit_element = model

            version_node_must_be_inserted = unit_for_sale.version() is not None and\
                                            unit_for_sale.version() != previous_unit_for_sale.version()
            if version_node_must_be_inserted:
                version = ET.SubElement(model, "version", display=unit_for_sale.version(), estado='activo')
                last_valid_parent_for_unit_element = version

            unit_node_must_be_inserted = self._must_insert_unit_element(unit_for_sale, previous_unit_for_sale)
            if unit_node_must_be_inserted:
                self._create_unit_element(last_valid_parent_for_unit_element, unit_for_sale)

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

    def _unit_data_exists(self, unit_for_sale):
        return unit_for_sale.has_valid_brand()

    def _create_unit_element(self, parent_node, unit_for_sale):
        if unit_for_sale.has_id():
            ET.SubElement(parent_node, "unidad", id=unit_for_sale.id())
        else:
            ET.SubElement(parent_node, "unidad")

    def _must_insert_unit_element(self, unit_for_sale, previous_unit_for_sale):
        if previous_unit_for_sale != unit_for_sale:
            return self._unit_data_exists(unit_for_sale)
        else:
            return False


