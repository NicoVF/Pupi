from django.urls import path

from .views import SendCatalogView, ConvertCSVView, NormalizeAndSortCSVView, GetUnitsWithLocalizationArguments, \
    VerificarPhone, WebhookWhatsapp

app_name = 'polls'
urlpatterns = [
    path('catalog/normalizeAndSort', NormalizeAndSortCSVView.as_view(), name='NormalizeAndSortCSV'),
    path('catalog/convert', ConvertCSVView.as_view(), name='ConvertCSV'),
    path('catalog/send', SendCatalogView.as_view(), name='SendCatalog'),
    path('catalog/getUnitsWithLocalizationArguments', GetUnitsWithLocalizationArguments.as_view(),
         name="getUnitsWithLocalizationArguments"),
    path('verificador/verificarTelefono', VerificarPhone.as_view(), name='VerificarPhone'),
    path('verificador/webhookWhatsapp', WebhookWhatsapp.as_view(), name='WebhookWhatsapp')

]