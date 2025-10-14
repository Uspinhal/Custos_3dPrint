from django.urls import path
from . import views

app_name = 'equipamentos'

urlpatterns = [
    path('', views.lista_equipamentos, name='lista'),
    path('criar/', views.criar_equipamento, name='criar'),
    path('<int:equipamento_id>/editar/', views.editar_equipamento, name='editar'),
    path('<int:equipamento_id>/deletar/', views.deletar_equipamento, name='deletar'),
    path('fabricante/adicionar/ajax/', views.adicionar_fabricante_ajax, name='adicionar_fabricante_ajax'),
]
