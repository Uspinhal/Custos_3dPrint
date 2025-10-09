from django.contrib import admin
from .models import Fabricante, Equipamento   

# Register your models here.
@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    search_fields = ('nome',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'fabricante', 'data_aquisicao', 'custo_aquisicao', 'potencia_watts')
    search_fields = ('nome', 'modelo', 'fabricante__nome')
    list_filter = ('modelo', 'fabricante', 'data_aquisicao')