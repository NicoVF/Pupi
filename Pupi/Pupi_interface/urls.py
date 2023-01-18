from django.urls import path

from .views import SendCatalogView, ConvertCSVView

app_name = 'polls'
urlpatterns = [
    path('catalog/send', SendCatalogView.as_view(), name='SendCatalog'),
    path('catalog/convert', ConvertCSVView.as_view(), name='ConvertCSV'),
]