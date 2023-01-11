import xml.etree.ElementTree as ET


class UnitForSale:
    def __init__(self, brand, model, version, image, id):
        self._brand = brand
        self._model = model
        self._version = version
        self._image = image
        self._id = id

    def __eq__(self, other):
        return self._brand == other.brand() and self._model == other.model() and self._version == other.version()

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

    def image_url(self):
        return self._image

    def has_image(self):
        return self._image is not ""

    @classmethod
    def no_unit_for_sale(cls):
        return cls(brand=None, model="", version=None, image="", id=None)

    @classmethod
    def create_unit_from(cls, fields):
        return cls(brand=fields[0],
                   model=fields[1] if len(fields) > 1 else "",
                   version=fields[2] if len(fields) > 2 and fields[2] != "" else None,
                   image=fields[5] if len(fields) > 5 else "",
                   id=fields[6] if len(fields) > 6 else None)


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        previous_unit_for_sale = UnitForSale.no_unit_for_sale()
        for row in rows:
            fields = row.split(',')

            current_unit_for_sale = UnitForSale.create_unit_from(fields)

            brand_node_must_be_inserted = current_unit_for_sale.brand() != previous_unit_for_sale.brand()
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=current_unit_for_sale.brand(), estado='activo')

            model_node_must_be_inserted = brand_node_must_be_inserted or current_unit_for_sale.model() != previous_unit_for_sale.model()
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=current_unit_for_sale.model(), estado='activo')
                last_valid_parent_for_unit_element = model

            version_node_must_be_inserted = current_unit_for_sale.version() is not None and\
                                            current_unit_for_sale.version() != previous_unit_for_sale.version()
            if version_node_must_be_inserted:
                version = ET.SubElement(model, "version", display=current_unit_for_sale.version(), estado='activo')
                last_valid_parent_for_unit_element = version

            unit_node_must_be_inserted = self._must_insert_unit_element(current_unit_for_sale, previous_unit_for_sale)
            if unit_node_must_be_inserted:
                self._create_unit_element(last_valid_parent_for_unit_element, current_unit_for_sale)

            previous_unit_for_sale = current_unit_for_sale
        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml

    def _unit_data_exists(self, unit_for_sale):
        return unit_for_sale.has_valid_brand()

    def _create_unit_element(self, parent_node, unit_for_sale):
        if unit_for_sale.has_id():
            unit = ET.SubElement(parent_node, "unidad", id=unit_for_sale.id())
        else:
            unit = ET.SubElement(parent_node, "unidad")
        image_node_must_be_inserted = unit_for_sale.has_image()
        if image_node_must_be_inserted:
            image = ET.SubElement(unit, "imagenes")
            url = ET.SubElement(image, "url", tipo="foto-agencia")
            url.text = unit_for_sale.image_url()

    def _must_insert_unit_element(self, unit_for_sale, previous_unit_for_sale):
        if previous_unit_for_sale != unit_for_sale:
            return self._unit_data_exists(unit_for_sale)
        else:
            return False


