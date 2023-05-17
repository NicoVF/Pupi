import os
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

        ip = self._get_ip(request)
        if not ip:
            return JsonResponse(
                {
                    "message": "ERROR - Se necesita un valor para el parametro ip"
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
        response = self._get_info_about(ip)

        if response['status'] == "fail":
            return JsonResponse(
                {
                    "message": "ERROR - IP invalida"
                })
        else:
            lat1, long1 = self._set_visitor_lat_and_long(response)
            country, region, city, _zip = self._set_visitor_country_region_city_and_zip(response)

        units_manager = UnitsManager()
        kms_around = 80
        filtered_units, amount_filtered_units, has_units_in_range = units_manager\
            .filter(brand=brand, model=model, lat1=lat1, long1=long1, year=year,
                    max_amount=max_amount, km_around=kms_around)
        filtered_units_json = units_manager.gen_json(filtered_units)

        info = \
            {
                "Mensaje": "OK",
                "IP": ip,
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
        return JsonResponse(info)

    def _set_visitor_lat_and_long(self, response):
        latitude = response['lat']
        longitude = response['lon']
        return latitude, longitude

    def _set_visitor_country_region_city_and_zip(self, response):
        country = response['country']
        region = response['regionName']
        city = response['city']
        _zip = response['zip']
        return country, region, city, _zip

    def _get_info_about(self, ip):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get("http://ip-api.com/json/" + ip + os.environ['KEY_GEOLOCATION_API'],
                                headers=headers).json()
        return response

    def _get_ip(self, request):
        return request.GET.get("ip")

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
