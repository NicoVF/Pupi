import requests
import os
import js2py
import lxml.etree as ET


class Unit:

    def __init__(self, brand, model, version, year, priceToShow, price, kilometers, currency,
                 image, _id, provider, providerOfProviders, idClient, entryDate):
        self._brand = brand
        self._model = model
        self._version = version
        self._year = year
        self._priceToShow = priceToShow
        self._price = price
        self._kilometers = kilometers
        self._currency = currency
        self._image = image
        self._id = _id
        self._provider = provider
        self._providerOfProviders = providerOfProviders
        self._idClient = idClient
        self._entryDate = entryDate

    def brand(self):
        return self._brand

    def model(self):
        return self._model

    def version(self):
        return self._version

    def year(self):
        return self._year

    def priceToShow(self):
        return self._priceToShow

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

    def provider(self):
        return self._provider

    def providerOfProviders(self):
        return self._providerOfProviders

    def idClient(self):
        return self._idClient

    def entryDate(self):
        return self._entryDate


class UnitsManager:

    def __init__(self):
        self._get_catalog()

    def filter(self, brand, model, lat1, long1, year, max_amount, km_around):
        catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
        units_filtered_in_range = []
        units_filtered_out_of_range = []
        brands = []
        models = []
        km_around = self.set_40_km_around_dont_has_brand_and_model(brand, km_around, model)
        brands = self._brands(brand, brands)
        models = self._models(model, models)

        for brand in brands:
            for model in models:
                versions = self._versions(brand=brand, model=model)
                for version in versions:
                    units_amount = self._units_amount(brand=brand, model=model,
                                                      version=version, year=year)
                    for i in range(units_amount):
                        unit = self._get_xpath_unit(brand, catalog, i, model, version, year)
                        unit_lat = self._get_attribute_value(unit, 'lat').replace(',', '.')
                        unit_long = self._get_attribute_value(unit, 'long').replace(',', '.')
                        if self._get_distance_in_km_between_localizations(lat1, long1, unit_lat, unit_long) > km_around:
                            self._create_and_append_unit(brand, model, unit, units_filtered_out_of_range, version)
                            if max_amount and len(units_filtered_out_of_range) == max_amount:
                                return units_filtered_out_of_range, len(units_filtered_out_of_range), False
                        else:
                            self._create_and_append_unit(brand, model, unit, units_filtered_in_range, version)
                            if max_amount and len(units_filtered_in_range) == max_amount:
                                return units_filtered_in_range, len(units_filtered_in_range), True

        if len(units_filtered_in_range) > 0:
            return units_filtered_in_range, len(units_filtered_in_range), True
        return units_filtered_out_of_range, len(units_filtered_out_of_range), False

    def set_40_km_around_dont_has_brand_and_model(self, brand, km_around, model):
        if not brand or not model:
            km_around = 40
        return km_around

    def _create_and_append_unit(self, brand, model, unit, units_filtered_out_of_range, version):
        unit = self._create_unit(unit, brand, model, version)
        units_filtered_out_of_range.append(unit)

    def _create_unit(self, unit, brand, model, version):
        unit_brand = brand
        unit_model = model
        unit_version = version
        unit_year = self._get_attribute_value(unit, "anio")
        unit_priceToShow = self._get_attribute_value(unit, "precioAMostrar")
        unit_price = self._get_attribute_value(unit, "precio")
        unit_currency = self._get_attribute_value(unit, "tipoCambio")
        unit_kilometers = self._get_attribute_value(unit, "kilometros")
        unit_image = self._get_subelement_value(unit, "imagenes/url")
        unit_id = self._get_attribute_value(unit, "id")
        unit_provider = self._get_attribute_value(unit, "cliente")
        unit_providerOfProviders = self._get_attribute_value(unit, "proveedorProveedores")
        unit_idClient = self._get_attribute_value(unit, "idDeCliente")
        unit_entryDate = self._get_attribute_value(unit, "fechaAlta")
        unit = Unit(unit_brand, unit_model, unit_version, unit_year, unit_priceToShow, unit_price,
                    unit_kilometers, unit_currency, unit_image, unit_id, unit_provider,
                    unit_providerOfProviders, unit_idClient, unit_entryDate)
        return unit

    def _get_xpath_unit(self, brand, catalog, i, model, version, year):
        if not year:
            unit = catalog.xpath(f"(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                 f"/version[@display='{version}']"
                                 f"/unidad[@lat][@long][@anio][@precioAMostrar][@precio]"
                                 f"[@tipoCambio][@kilometros][@id][@cliente])[{i + 1}]")
        else:
            unit = catalog.xpath(f"(//marca[@nombre='{brand}']/modelo[@display='{model}']"
                                 f"/version[@display='{version}']"
                                 f"/unidad[@lat][@long][@anio='{year}'][@precioAMostrar][@precio]"
                                 f"[@tipoCambio][@kilometros][@id][@cliente])[{i + 1}]")
        return unit

    def _units_amount(self, brand, model, version, year):
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

    def _brands(self, brand, brands):
        if not brand:
            catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
            brands = catalog.xpath(f"//marca/@nombre")
            return brands
        else:
            brands.append(brand)
            return brands

    def _models(self, model, models):
        if not model:
            catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
            models = catalog.xpath(f"//marca/modelo/@display")
            return models
        else:
            models.append(model)
            return models

    def _versions(self, brand, model):
        catalog = ET.parse('Pupi_interface/business/localization/catalogo-usados.xml')
        versions = catalog.xpath(f"//marca[@nombre='{brand}']/modelo[@display='{model}']/version/@display")
        return versions

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
        try:
            return element[0].attrib[f'{attribute_name}']
        except:
            return None

    def _get_subelement_value(self, element, path):
        try:
            return element[0].find(f'{path}').text
        except AttributeError:
            return None

    def gen_json(self, filtered_units):

        units = {}
        for i, unit in enumerate(filtered_units, 1):
            units[f"Unidad{i}"] = self._dictionary_for(unit)
        return units

    def _dictionary_for(self, unit):
        json_unit = {}
        json_unit["Marca"] = unit.brand()
        json_unit["Modelo"] = unit.model()
        json_unit["Version"] = unit.version()
        json_unit["Anio"] = unit.year()
        json_unit["PrecioAMostrar"] = unit.priceToShow()
        json_unit["Precio"] = unit.price()
        json_unit["Tipo_cambio"] = unit.currency()
        json_unit["Kilometraje"] = unit.kilometers()
        json_unit["Foto_agencia"] = unit.image()
        json_unit["ID"] = unit.id()
        json_unit["Proveedor"] = unit.provider()
        json_unit["ProveedorDeProveedores"] = unit.providerOfProviders()
        json_unit["ClienteID"] = unit.idClient()
        json_unit["FechaAlta"] = unit.entryDate()
        return json_unit
