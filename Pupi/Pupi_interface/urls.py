from django.urls import path

from .views import SendCatalogView

app_name = 'polls'
urlpatterns = [
    path('catalog/send', SendCatalogView.as_view(), name='SendCatalog'),
]