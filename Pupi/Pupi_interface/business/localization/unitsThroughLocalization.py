import requests
import os
import js2py
import lxml.etree as ET


class Unit:

    def __init__(self, brand, model, version, year, price, kilometers, currency, image, _id):
        self._brand = brand
        self._model = model
        self._version = version
        self._year = year
        self._price = price
        self._kilometers = kilometers
        self._currency = currency
        self._image = image
        self._id = _id

    def brand(self):
        return self._brand

    def model(self):
        return self._model

    def version(self):
        return self._version

    def year(self):
        return self._year

    def price(self):
        return self._price

    def kilometers(self):
        return self._kilometers

    def currency(self):
        return self._currency

    def image(self):
        return self._image

    def id(self):
        return self._id


class UnitsManager:

    def __init__(self):
        self._get_catalog()

    def filter(self, brand, model, lat1, long1, year, max_amount):
        catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
        units_filtered = []

        versions = self._versions_of_model(brand=brand, model=model)
        for version in versions:
            units_amount = self._units_amount_of_model_and_version(brand=brand, model=model,
                                                                   version=version, year=year)
            for i in range(units_amount):
                unit = self._get_xpath_unit(brand, catalog, i, model, version, year)
                unit_lat = self._get_attribute_value(unit, 'lat').replace(',', '.')
                unit_long = self._get_attribute_value(unit, 'long').replace(',', '.')
                if self._get_distance_in_km_between_localizations(lat1, long1, unit_lat, unit_long) > 70:
                    continue
                else:
                    unit = self._create_unit(unit, brand, model, version)
                    units_filtered.append(unit)
                    if max_amount and len(units_filtered) == max_amount:
                        return units_filtered, len(units_filtered)

        return units_filtered, len(units_filtered)

    def _create_unit(self, unit, brand, model, version):
        unit_brand = brand
        unit_version = version
        unit_year = self._get_attribute_value(unit, "anio")
        unit_price = self._get_attribute_value(unit, "precio")
        unit_currency = self._get_attribute_value(unit, "tipoCambio")
        unit_kilometers = self._get_attribute_value(unit, "kilometros")
        unit_image = self._get_subelement_value(unit, "imagenes/url")
        unit_id = self._get_attribute_value(unit, "id")
        unit = Unit(unit_brand, model, unit_version, unit_year, unit_price,
                    unit_kilometers, unit_currency, unit_image, unit_id)
        return unit

    def _get_xpath_unit(self, brand, catalog, i, model, version, year):
        if not year:
            unit = catalog.xpath(f"(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                 f"/version[@display='{version}']"
                                 f"/unidad[@lat][@long][@anio][@precio][@tipoCambio][@kilometros][@id])[{i + 1}]")
        else:
            unit = catalog.xpath(f"(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                 f"/version[@display='{version}']"
                                 f"/unidad[@lat][@long][@anio='{year}'][@precio]"
                                 f"[@tipoCambio][@kilometros][@id])[{i + 1}]")
        return unit

    def _units_amount_of_model_and_version(self, brand, model, version, year):
        catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
        amount = None
        if not year:
            amount = int(catalog.xpath(f"count(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                       f"/version[@display='{version}']"
                                       f"/unidad[@lat][@long][@anio][@precio][@kilometros][@tipoCambio][@id])"))
        if year:
            amount = int(catalog.xpath(f"count(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                       f"/version[@display='{version}']"
                                       f"/unidad[@lat][@long][@anio={year}][@precio][@kilometros][@tipoCambio][@id])"))
        return amount

    def _versions_of_model(self, brand, model):
        catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
        amount = catalog.xpath(f"//marca[@nombre='{brand}']/modelo[@display='{model}']/version/@display")
        return amount

    def _get_catalog(self):

        headers = {
            "X-SOYBOT-TOKEN": os.environ['PROD_RUN_CAT_USADO_TOKEN']
        }
        response = requests.get(os.environ['URL_PROD_RUN_CAT_USADO'], headers=headers)

        with open("Pupi_interface/business/localization/catalogo-usados.xml", "wb") as file:
            file.write(response.content)
        file.close()

    def _get_distance_in_km_between_localizations(self, lat1, long1, lat2, long2):
        eval_res, file = js2py.run_file("Pupi_interface/business/localization/localization.js")
        km_distance = file.getDistanceFromLatLonInKm(lat1, long1, lat2, long2)
        return km_distance

    def _get_attribute_value(self, element, attribute_name):
        return element[0].attrib[f'{attribute_name}']

    def _get_subelement_value(self, element, path):
        try:
            return element[0].find(f'{path}').text
        except AttributeError:
            return None

    def gen_json(self, filtered_units):
        global units
        units = {}
        for i, unit in enumerate(filtered_units, 1):
            json_unit = self._get_json_unit_template()
            json_unit = self._set_values_in(json_unit, unit)
            self._add_json_unit_in_json_units(i, json_unit, units)
        return units

    def _add_json_unit_in_json_units(self, i, json_unit, units):
        units.update({f"Unidad{i}": json_unit})

    def _set_values_in(self, json_unit, unit):
        json_unit["Version"] = unit.version()
        json_unit["Anio"] = unit.year()
        json_unit["Precio"] = unit.price()
        json_unit["Tipo_cambio"] = unit.currency()
        json_unit["Kilometraje"] = unit.kilometers()
        json_unit["Foto_agencia"] = unit.image()
        json_unit["ID"] = unit.id()
        return json_unit

    def _get_json_unit_template(self):
        unit_template = {
            "Version": None,
            "Anio": None,
            "Precio": None,
            "Tipo_cambio": None,
            "Kilometraje": None,
            "Foto_agencia": None,
            "ID": None,
        }
        return unit_template
