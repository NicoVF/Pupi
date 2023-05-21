import os
import re

import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views import generic

from Pupi_interface.api_calls.dollar_value import DollarValue
from Pupi_interface.business import Result, Cliente
from Pupi_interface.business.remote_pupi import RemotePupi
from Pupi_interface.business.localization.unitsThroughLocalization import UnitsManager


# Create your views here.

class SendCatalogView(generic.TemplateView):
    template_name = 'templates/sendCatalog.html'

    def get(self, request, *args, **kwargs):
        titulo = 'Enviar Catalogo'
        client_name = "PROD-RUN"
        sucursal = "SERGI"
        token = "c949c975-5445-4bdc-8616-54a74015dc1c"
        context = {
            'title': titulo,
            'errors': "",
            'xml': "",
            'client_name': client_name,
            'token': token,
            'sucursal': sucursal
        }
        return render(request, 'templates/sendCatalog.html', context)

    def post(self, request, *args, **kwargs):
        # obtengo parametros
        xml_to_send = request.POST["xml"]

        # ejecuto lo que tengo que ejecutar
        client_name = request.POST["client_name"]
        sucursal = request.POST["sucursal"]
        token = request.POST["token"]
        client = Cliente(client_name, sucursal, token)
        pupi = RemotePupi()
        result = Result()
        result = pupi.send_xml(client, xml_to_send)
        result_errors = str(result.errors())

        # construir respuesta
        titulo = 'Enviar Catalogo'
        context = {
            'title': titulo,
            'errors': result_errors,
            'xml': xml_to_send,
            'client_name': client_name,
            'token': token,
            'sucursal': sucursal
        }
        return render(request, 'templates/sendCatalog.html', context)


class ConvertCSVView(generic.TemplateView):
    template_name = 'templates/convertCSVtoXML.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # obtengo parametros
        csv_to_convert = request.POST["csv"]

        # ejecuto lo que tengo que ejecutar
        pupi = RemotePupi()
        xml = pupi.convert_to_xml(csv_to_convert)

        # construir respuesta
        titulo = 'Enviar Catalogo'
        context = {
            'title': titulo,
            'errors': [],
            'xml': xml,
            'client_name': "",
            'token': "",
            'sucursal': ""
        }
        return render(request, 'templates/sendCatalog.html', context)


class NormalizeAndSortCSVView(generic.TemplateView):
    template_name = 'templates/normalizeAndSortCSV.html'

    def get(self, request, *args, **kwargs):
        valor_dolar = DollarValue().dollar_value()
        context = {
            'cotizacion_dolar': valor_dolar
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # obtengo parametros
        csv_to_normalize_and_sort = request.POST["csv"]
        cotizacion_dolar_string = request.POST["cotizacion_dolar"]
        try:
            cotizacion_dolar_int = int(cotizacion_dolar_string)
        except:
            raise ValueError(f"Ingrese un valor numerico para la cotizacion del dolar")

        # ejecuto lo que tengo que ejecutar
        pupi = RemotePupi()
        pupi.set_usd_in_ars(cotizacion_dolar_int)
        normalized_and_sorted_csv = pupi.normalize_and_sort_csv(csv_to_normalize_and_sort)

        # construir respuesta
        context = {
            'csv': normalized_and_sorted_csv,
            'cotizacion_dolar': cotizacion_dolar_string
        }
        return render(request, 'templates/convertCSVtoXML.html', context)


class GetUnitsWithLocalizationArguments(View):

    def get(self, request):

        if not self._get_token(request):
            return JsonResponse(
                {
                    "message": "ERROR - Acceso denegado"
                })

        ip, phone = self._get_ip_or_phone(request)
        if not ip and not phone:
            return JsonResponse(
                {
                    "message": "ERROR - Se necesita un valor para el parametro ip o telefono"
                })

        brand = self._get_brand(request)
        if not brand:
            return JsonResponse(
                {
                    "message": "ERROR - Se necesita un valor para el parametro marca"
                })

        model = self._get_model(request)
        if not model:
            return JsonResponse(
                {
                    "message": "ERROR - Se necesita un valor para el parametro modelo"
                })

        year = self._get_year(request)
        max_amount = self._get_max_amount(request)

        units_manager = UnitsManager()
        kms_around = 80

        if ip:
            ip_info_response = self._get_info_about_ip(ip)

            if ip_info_response['status'] == "fail":
                return JsonResponse(
                    {
                        "message": "ERROR - IP invalida"
                    })
            else:
                country, region, city, _zip = self._set_visitor_country_region_city_and_zip_from_ip(ip_info_response)
                lat1, long1 = self._set_visitor_lat_and_long_from_ip(ip_info_response)

            info = self._get_filtered_info(units_manager, ip, phone, brand, model, year, max_amount, kms_around, lat1,
                                           long1, country, region, city, _zip)

            return JsonResponse(info)

        if phone and not ip:
            phone_info_response = self._get_info_about_phone(phone)
            if "error" in phone_info_response:
                return JsonResponse(
                    {
                        "message": "ERROR - Telefono invalido"
                    })
            else:
                country, region, city, _zip = self._set_visitor_country_region_city_and_zip_from_phone(phone_info_response)
                lat1, long1 = self._set_visitor_lat_and_long_from_phone(region + " " + city)

            info = self._get_filtered_info(units_manager, ip, phone, brand, model, year, max_amount, kms_around, lat1,
                                           long1, country, region, city, _zip)

            return JsonResponse(info)

    def _get_filtered_info(self, units_manager, ip, phone, brand, model, year, max_amount, kms_around, lat1, long1,
                           country, region, city, _zip):
        filtered_units, amount_filtered_units, has_units_in_range = units_manager \
            .filter(brand=brand, model=model, lat1=lat1, long1=long1, year=year,
                    max_amount=max_amount, km_around=kms_around)
        filtered_units_json = units_manager.gen_json(filtered_units)
        info = \
            {
                "Mensaje": "OK",
                "IP": ip,
                "Telefono": phone,
                "Pais": country,
                "Provincia": region,
                "Ciudad": city,
                "CP": _zip,
                "Marca": brand,
                "Modelo": model,
                "Unidades segun distancia": has_units_in_range,
                "Cantidad de unidades": amount_filtered_units,
                "Unidades": filtered_units_json
            }
        return info

    def _set_visitor_lat_and_long_from_ip(self, response):
        latitude = response['lat']
        longitude = response['lon']
        return latitude, longitude

    def _set_visitor_country_region_city_and_zip_from_ip(self, response):
        country = response['country']
        region = response['regionName']
        city = response['city']
        _zip = response['zip']
        return country, region, city, _zip

    def _get_info_about_ip(self, ip):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get("http://ip-api.com/json/" + ip + os.environ['KEY_GEOLOCATION_API'],
                                headers=headers).json()
        return response

    def _get_info_about_phone(self, phone):
        body = f"<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    <s:Body>\r\n        " \
               f"<Normalizar xmlns=\"http://tempuri.org/\">\r\n            <sXml>\r\n                &lt;xml&gt;\r\n" \
               f"                    &lt;telefonos&gt;\r\n                        &lt;telefono codigo=&quot;1&quot; " \
               f"prefijopais=&quot;+54&quot;&gt;{phone}&lt;/telefono&gt;\r\n                    &lt;/telefonos&gt;" \
               f"\r\n                &lt;/xml&gt;\r\n            </sXml>\r\n        " \
               f"</Normalizar>\r\n    </s:Body>\r\n</s:Envelope>"
        headers = {'Content-Type': 'text/xml', 'SOAPAction': 'http://tempuri.org/IService1/Normalizar'}
        response = requests.post(os.environ['URL_COVER_NORMALIZATION_API'], headers=headers, data=body).text
        return response

    def _get_ip_or_phone(self, request):
        ip = request.GET.get("ip")
        tel = request.GET.get("telefono")
        return ip, tel

    def _get_model(self, request):
        return request.GET.get("modelo")

    def _get_brand(self, request):
        return request.GET.get("marca")

    def _get_max_amount(self, request):
        try:
            max_cant = int(request.GET.get("cantidad_max"))
        except TypeError:
            max_cant = None
        return max_cant

    def _get_year(self, request):
        try:
            anio = int(request.GET.get("anio"))
        except TypeError:
            anio = None
        return anio

    def _get_token(self, request):
        return request.GET.get("token") == os.environ['TOKEN_API_UNITS_THROUGH_LOCALIZATION']

    def _set_visitor_lat_and_long_from_phone(self, region_and_city):
        lat, long = self._get_lat_long_of(region_and_city)
        return lat, long

    def _get_lat_long_of(self, region_and_city):
        headers = {'Accept': 'application/json'}
        params = {'region': 'ar', 'query': f'{region_and_city}', 'key': os.environ['KEY_GOOGLE_MAPS_API_TEXT_SEARCH']}
        response = requests.get(os.environ['URL_GOOGLE_MAPS_API_TEXT_SEARCH'], headers=headers, params=params).json()
        lat = response['results'][0]['geometry']['location']['lat']
        long = response['results'][0]['geometry']['location']['lng']
        return lat, long

    def _set_visitor_country_region_city_and_zip_from_phone(self, phone_info_response):
        country = None
        _zip = None
        province = re.search("(?<=Provincia=\")(\w+|(\w+\W\w+)+)(?=\")", phone_info_response).group(0)
        city = re.search("(?<=Localidad=\")(\w+|(\w+\W\w+)+)(?=\")", phone_info_response).group(0)
        return country, province, city, _zip
