from django.shortcuts import render
from django.views import generic

from Pupi.Pupi_interface.tests import Pupi, Cliente


# Create your views here.

class SendCatalogView(generic.TemplateView):
    template_name = 'templates/sendCatalog.html'

    def get(self, request, *args, **kwargs):
        titulo = 'Enviar Catalogo'
        context = {"title": titulo, 'errors': "", 'xml': ""}
        return render(request, 'templates/sendCatalog.html', context)

    def post(self, request, *args, **kwargs):
        # obtengo parametros

        # ejecuto lo que tengo que ejecutar
        client_name = "PROD-RUN"
        sucursal = "SERGI"
        token = "c949c975-5445-4bdc-8616-54a74015dc1c"
        client = Cliente(client_name, sucursal, token)
        pupi = Pupi()
        result = Result()
        xml_to_send = ""
        result = pupi.enviar_xml(client, xml_to_send)

        # construir respuesta
        titulo = 'Enviar Catalogo'
        context = {"title": titulo, 'errors': result.errors()[0], 'xml': xml_to_send}
        return render(request, 'templates/sendCatalog.html', context)
