from django.urls import path

from .views import SendCatalogView, ConvertCSVView, NormalizeAndSortCSVView

app_name = 'polls'
urlpatterns = [
    path('catalog/send', SendCatalogView.as_view(), name='SendCatalog'),
    path('catalog/convert', ConvertCSVView.as_view(), name='ConvertCSV'),
    path('catalog/normalizeAndSort', NormalizeAndSortCSVView.as_view(), name='NormalizeAndSortCSV'),
]