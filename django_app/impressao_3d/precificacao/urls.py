from django.urls import path
from . import views

app_name = 'precificacao'

urlpatterns = [
    path('',                          views.lista_orcamentos,  name='lista'),
    path('novo/',                     views.criar_orcamento,   name='criar'),
    path('<int:orcamento_id>/',        views.detalhe_orcamento, name='detalhe'),
    path('<int:orcamento_id>/editar/', views.editar_orcamento,  name='editar'),
    path('<int:orcamento_id>/deletar/',views.deletar_orcamento, name='deletar'),
    path('<int:orcamento_id>/enviar/', views.enviar_orcamento, name='enviar'),
]