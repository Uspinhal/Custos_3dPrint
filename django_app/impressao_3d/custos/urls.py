# custos/urls.py
from django.urls import path
from .views import calcular_custo_view, CalcularCustoAPI

urlpatterns = [
    path("api/calcular/", CalcularCustoAPI.as_view(), name="api_calcular_custo"),
    path("calcular/", calcular_custo_view, name="calcular_custo_form"),
]
