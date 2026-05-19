from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # -------------------------
    # Pedidos
    # -------------------------
    path('',                        views.lista_pedidos,  name='lista'),
    path('novo/',                   views.novo_pedido,    name='novo'),
    path('<int:pedido_id>/',         views.detalhe_pedido, name='detalhe'),
    path('<int:pedido_id>/editar/',  views.editar_pedido,  name='editar'),
    path('<int:pedido_id>/enviado/', views.marcar_enviado, name='marcar_enviado'),

    # -------------------------
    # Ordens de Produção
    # -------------------------
    path('ordens/',                       views.lista_ordens,  name='lista_ordens'),
    path('ordens/nova/',                  views.nova_ordem,    name='nova_ordem'),
    path('ordens/<int:ordem_id>/',        views.detalhe_ordem, name='detalhe_ordem'),
    path('ordens/<int:ordem_id>/editar/', views.editar_ordem,  name='editar_ordem'),
]