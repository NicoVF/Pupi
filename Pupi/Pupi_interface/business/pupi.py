import csv
import xml.etree.ElementTree as ET


class UnitForSale:
    NO_BRAND = None
    NO_MODEL = ""
    NO_VERSION = None
    NO_YEAR = ""
    NO_PRICE = ""
    NO_IMAGE = ""
    NO_ID = ""
    NO_KILOMETERS = ""
    NO_CURRENCY = ""
    NO_ZONE = ""
    NO_LATITUD = ""
    NO_LONGITUD = ""
    NO_PROVIDER = ""
    NO_PROVIDER_OF_PROVIDERS = ""
    NO_SALES_TYPE = ""

    def __init__(self, brand, model, version, year, price, image, id, kilometers, currency, zone, latitud, longitud, provider, provider_of_providers, sales_type):
        self._brand = brand
        self._model = model
        self._version = version
        self._year = year
        self._price = price
        self._image = image
        self._id = id
        self._kilometers = kilometers
        self._currency = currency
        self._zone = zone
        self._latitud = latitud
        self._longitud = longitud
        self._provider = provider
        self._provider_of_providers = provider_of_providers
        self._sales_type = sales_type
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
        return self._id != self.NO_ID

    def year(self):
        return self._year

    def has_year(self):
        return self._year != self.NO_YEAR

    def kilometers(self):
        return self._kilometers

    def has_kilometers(self):
        return self._kilometers != self.NO_KILOMETERS

    def currency(self):
        return self._currency

    def has_currency(self):
        return self._currency != self.NO_CURRENCY
    
    def zone(self):
        return self._zone

    def has_zone(self):
        return self._zone != self.NO_ZONE

    def latitud(self):
        return self._latitud

    def has_latitud(self):
        return self._latitud != self.NO_LATITUD

    def longitud(self):
        return self._longitud

    def has_longitud(self):
        return self._longitud != self.NO_LONGITUD

    def provider(self):
        return self._provider

    def has_provider(self):
        return self._provider != self.NO_PROVIDER

    def provider_of_providers(self):
        return self._provider_of_providers

    def has_provider_of_providers(self):
        return self._provider_of_providers != self.NO_PROVIDER_OF_PROVIDERS

    def sales_type(self):
        return self._sales_type

    def has_sales_type(self):
        return self._sales_type != self.NO_SALES_TYPE
    
    def price(self):
        return self._price

    def has_price(self):
        return self._price != self.NO_PRICE

    def has_valid_brand(self):
        return self._brand is not self.NO_BRAND

    def image_url(self):
        return self._image

    def has_image(self):
        return self._image is not self.NO_IMAGE

    @classmethod
    def no_unit_for_sale(cls):
        return cls(brand=cls.NO_BRAND, model=cls.NO_MODEL, version=cls.NO_VERSION, year=cls.NO_YEAR, price=cls.NO_PRICE,
                   image=cls.NO_IMAGE, id=cls.NO_ID, kilometers=cls.NO_KILOMETERS, currency=cls.NO_CURRENCY,
                   zone=cls.NO_ZONE, latitud=cls.NO_LATITUD, longitud=cls.NO_LONGITUD, provider=cls.NO_PROVIDER,
                   provider_of_providers=cls.NO_PROVIDER_OF_PROVIDERS, sales_type=cls.NO_SALES_TYPE)

    @classmethod
    def create_unit_from(cls, fields):
        return cls(brand=fields[0],
                   model=fields[1] if len(fields) > 1 else cls.NO_MODEL,
                   version=fields[2] if len(fields) > 2 and fields[2] != "" else cls.NO_VERSION,
                   year=fields[3] if len(fields) > 3 else cls.NO_YEAR,
                   price=fields[4] if len(fields) > 4 else cls.NO_PRICE,
                   image=fields[5] if len(fields) > 5 else cls.NO_IMAGE,
                   id=fields[6] if len(fields) > 6 else cls.NO_ID,
                   kilometers=fields[7] if len(fields) > 7 else cls.NO_KILOMETERS,
                   currency=fields[8] if len(fields) > 8 else cls.NO_CURRENCY,
                   zone=fields[9] if len(fields) > 9 else cls.NO_ZONE,
                   latitud=fields[10] if len(fields) > 10 else cls.NO_LATITUD,
                   longitud=fields[11] if len(fields) > 11 else cls.NO_LONGITUD,
                   provider=fields[12] if len(fields) > 12 else cls.NO_PROVIDER,
                   provider_of_providers=fields[13] if len(fields) > 13 else cls.NO_PROVIDER_OF_PROVIDERS,
                   sales_type=fields[14] if len(fields) > 14 else cls.NO_SALES_TYPE,
                   )


class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, a_csv):
        normalized_csv = self._normalize_csv(a_csv)
        rows = csv.reader(normalized_csv.splitlines())
        brands = ET.Element("marcas", xmlns='http://chat.soybot.com/catalogo/V1')
        previous_unit_for_sale = UnitForSale.no_unit_for_sale()
        for fields in rows:

            current_unit_for_sale = UnitForSale.create_unit_from(fields)

            brand_node_must_be_inserted = current_unit_for_sale.brand() != previous_unit_for_sale.brand()
            if brand_node_must_be_inserted:
                brand = ET.SubElement(brands, "marca", nombre=current_unit_for_sale.brand().capitalize(), estado='activo')

            model_node_must_be_inserted = brand_node_must_be_inserted or current_unit_for_sale.model() != previous_unit_for_sale.model()
            if model_node_must_be_inserted:
                model = ET.SubElement(brand, "modelo", display=current_unit_for_sale.model().capitalize(),
                                      estado='activo', enlista='activo', id=current_unit_for_sale.model().lower())
                last_valid_parent_for_unit_element = model

            version_node_must_be_inserted = current_unit_for_sale.version() is not None and\
                                            current_unit_for_sale.version() != previous_unit_for_sale.version()
            if version_node_must_be_inserted:
                version = ET.SubElement(model, "version", display=current_unit_for_sale.version().capitalize(),
                                        estado='activo', enlista='activo', id=current_unit_for_sale.version().lower())
                last_valid_parent_for_unit_element = version

            unit_node_must_be_inserted = self._must_insert_unit_element(current_unit_for_sale, previous_unit_for_sale)
            if unit_node_must_be_inserted:
                self._create_unit_element(last_valid_parent_for_unit_element, current_unit_for_sale)

            previous_unit_for_sale = current_unit_for_sale
        ET.indent(brands, space='    ')
        xml = ET.tostring(brands, encoding="utf-8", method='xml', xml_declaration=True, ).decode('utf-8')
        return xml

    def _normalize_csv(self, a_csv):
        rows = csv.reader(a_csv.splitlines())
        normalized_rows = []
        for fields in rows:
            normalized_fields = fields
            normalized_fields[0] = normalized_fields[0].capitalize()
            if len(fields) > 1:
                normalized_fields[1] = normalized_fields[1].capitalize()
            quoted_fields = ("\"" + field + "\"" for field in normalized_fields)
            normalized_row = ",".join(quoted_fields)
            normalized_rows.append(normalized_row)
        normalized_csv = "\n".join(normalized_rows)

        return normalized_csv

    def _unit_data_exists(self, unit_for_sale):
        return unit_for_sale.has_valid_brand()

    def _create_unit_xml_element(self, parent_node, unit_for_sale):
        unit_attr = {}
        if unit_for_sale.has_id():
            unit_attr["id"] = unit_for_sale.id()
        if unit_for_sale.has_kilometers():
            unit_attr["kilometros"] = unit_for_sale.kilometers()
        if unit_for_sale.has_year():
            unit_attr["anio"] = unit_for_sale.year()
        if unit_for_sale.has_price():
            unit_attr["precio"] = unit_for_sale.price()
        if unit_for_sale.has_currency():
            unit_attr["tipoCambio"] = unit_for_sale.currency()
        if unit_for_sale.has_zone():
            unit_attr["zona"] = unit_for_sale.zone()
        if unit_for_sale.has_latitud():
            unit_attr["lat"] = unit_for_sale.latitud()
        if unit_for_sale.has_longitud():
            unit_attr["long"] = unit_for_sale.longitud()
        if unit_for_sale.has_provider():
            unit_attr["cliente"] = unit_for_sale.provider()
        if unit_for_sale.has_provider_of_providers():
            unit_attr["proveedorProveedores"] = unit_for_sale.provider_of_providers()
        if unit_for_sale.has_sales_type():
            unit_attr["tipoVenta"] = unit_for_sale.sales_type()
        unit = ET.SubElement(parent_node, "unidad", **unit_attr)
        return unit

    def _create_unit_element(self, parent_node, unit_for_sale):
        parameters = {"parent_node": parent_node, "unit_for_sale": unit_for_sale}
        unit = self._create_unit_xml_element(**parameters)
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

    def _practica(self):
        row = ""
        unit_for_sale = self.row_to_unit(row)
        xml_element = self.unit_to_xml(unit_for_sale)
        formatted_xml_element = self.format_xml(xml_element)
    def _practica(self):
        row = ""
        unit_for_sale = self.row_to_unit(row)
        formatted_unit = self.format_unit(unit_for_sale)
        xml_element = self.unit_to_xml(formatted_unit)



