from django.shortcuts import render
from django.views import generic

from Pupi_interface.business import Result, Cliente
from Pupi_interface.business.simulated_pupi import SimulatedPupi
from Pupi_interface.business.remote_pupi import RemotePupi


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

