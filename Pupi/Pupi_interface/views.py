from django.shortcuts import render
from django.views import generic


class Result:
    def __init__(self):
        self._errors = []

    def add_error(self, error):
        self._errors.append(error)

    def is_succesfull(self):
        return len(self._errors) == 0

    def errors(self):
        return self._errors


class Pupi:
    def enviar_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("Root element is missing.")
        return result


class Cliente:
    def __init__(self, cliente, sucursal, token):
        pass


# Create your views here.

class SendCatalogView(generic.TemplateView):
    template_name = 'templates/sendCatalog.html'

    def get(self, request, *args, **kwargs):
        titulo = 'Enviar Catalogo'
        context = {"title": titulo, 'errors': "", 'xml': ""}
        return render(request, 'templates/sendCatalog.html', context)

    def post(self, request, *args, **kwargs):
        # obtengo parametros
        xml_to_send = request.POST["xml"]

        # ejecuto lo que tengo que ejecutar
        client_name = "PROD-RUN"
        sucursal = "SERGI"
        token = "c949c975-5445-4bdc-8616-54a74015dc1c"
        client = Cliente(client_name, sucursal, token)
        pupi = Pupi()
        result = Result()
        result = pupi.enviar_xml(client, xml_to_send)
        result_errors = str(result.errors())

        # construir respuesta
        titulo = 'Enviar Catalogo'
        context = {"title": titulo, 'errors': result_errors, 'xml': xml_to_send}
        return render(request, 'templates/sendCatalog.html', context)

