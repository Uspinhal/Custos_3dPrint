from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # Matérias-primas
    path('materias-primas/', views.lista_materias_primas, name='lista_materias_primas'),
    path('materias-primas/criar/', views.criar_materia_prima, name='criar_materia_prima'),
    path('materias-primas/editar/<int:materia_id>/', views.editar_materia_prima, name='editar_materia_prima'),
    path('materias-primas/deletar/<int:materia_id>/', views.deletar_materia_prima, name='deletar_materia_prima'),

    # Insumos
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('insumos/criar/', views.criar_insumo, name='criar_insumo'),
    path('insumos/editar/<int:insumo_id>/', views.editar_insumo, name='editar_insumo'),
    path('insumos/deletar/<int:insumo_id>/', views.deletar_insumo, name='deletar_insumo'),
    path('materias-primas/compras/<int:compra_id>/editar/', views.editar_compra_materia, name='editar_compra_materia'),
    path('materias-primas/compras/<int:compra_id>/deletar/', views.deletar_compra_materia, name='deletar_compra_materia'),

    # Compras Matéria-Prima
    path('materias-primas/compras/', views.lista_compras_materia, name='lista_compras_materia'),
    path('materias-primas/compras/criar/', views.criar_compra_materia, name='criar_compra_materia'),

    # Compras Insumos
    path('insumos/compras/', views.lista_compras_insumo, name='lista_compras_insumo'),
    path('insumos/compras/criar/', views.criar_compra_insumo, name='criar_compra_insumo'),
    path('insumos/compras/<int:compra_id>/editar/', views.editar_compra_insumo, name='editar_compra_insumo'),
    path('insumos/compras/<int:compra_id>/deletar/', views.deletar_compra_insumo, name='deletar_compra_insumo'),
]