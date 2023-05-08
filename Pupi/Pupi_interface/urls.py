from django.urls import path

from .views import SendCatalogView, ConvertCSVView, NormalizeAndSortCSVView, GetUnitsWithLocalizationArguments

app_name = 'polls'
urlpatterns = [
    path('catalog/normalizeAndSort', NormalizeAndSortCSVView.as_view(), name='NormalizeAndSortCSV'),
    path('catalog/convert', ConvertCSVView.as_view(), name='ConvertCSV'),
    path('catalog/send', SendCatalogView.as_view(), name='SendCatalog'),
    path('catalog/getUnitsWithLocalizationArguments', GetUnitsWithLocalizationArguments.as_view(),
         name="getUnitsWithLocalizationArguments")

]