from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('custos/', include('custos.urls')),
    path('equipamentos/', include(('equipamentos.urls', 'equipamentos'), namespace='equipamentos')),
    path('', include(('estoque.urls', 'estoque'), namespace='estoque')), 
]
