from django.contrib import admin
from .models import Insumos, MateriaPrima, Marca

# Register your models here.
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'material', 'cor', 'marca', 'quantidade', 'estoque_minimo', 'preco')
    list_filter = ('tipo', 'material', 'cor', 'marca')
    search_fields = ('nome', 'material', 'cor', 'marca__nome')
    autocomplete_fields = ('marca',)

@admin.register(Insumos)
class InsumosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'quantidade', 'estoque_minimo', 'preco_unitario', 'quantidade_minima')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo')
