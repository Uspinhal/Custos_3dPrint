from django.contrib import admin
from .models import Marca, MateriaPrima, CompraMateriaPrima, Insumos, CompraInsumo
# Register your models here.

# ==========================
# INLINE: Histórico de Compras
# ==========================

class CompraMateriaPrimaInline(admin.TabularInline):
    model = CompraMateriaPrima
    extra = 1
    fields = ("data_compra", "quantidade", "preco_total", "preco_unitario_display")
    readonly_fields = ("preco_unitario_display",)

    def preco_unitario_display(self, obj):
        return f"R$ {obj.preco_unitario():.2f}" if obj.pk else "-"
    preco_unitario_display.short_description = "Preço Unitário"


class CompraInsumoInline(admin.TabularInline):
    model = CompraInsumo
    extra = 1
    fields = ("data_compra", "quantidade", "preco_total", "preco_unitario_display")
    readonly_fields = ("preco_unitario_display",)

    def preco_unitario_display(self, obj):
        return f"R$ {obj.preco_unitario():.2f}" if obj.pk else "-"
    preco_unitario_display.short_description = "Preço Unitário"

# ==========================
# ADMIN: MateriaPrima
# ==========================
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
         'tipo', 
         'material', 
         'cor', 
         'marca', 
         'quantidade', 
         'estoque_minimo', 
         'preco_total', 
         'preco_unitario', 
         'unidade',
         "preco_unitario_display")
    list_filter = ('tipo', 'material', 'cor', 'marca')
    search_fields = ('nome', 'material', 'cor', 'marca__nome')
    readonly_fields = ("preco_unitario_display",)
    autocomplete_fields = ('marca',)
    inlines = [CompraMateriaPrimaInline]

    def preco_unitario_display(self, obj):
        return f"R$ {obj.preco_unitario:.2f}" if obj.preco_unitario else "-"
    preco_unitario_display.short_description = "Preço Unitário Atual"

# ==========================
# ADMIN: Insumos
# ==========================

@admin.register(Insumos)
class InsumosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'categoria', 'preco_unitario', 'peso_no_calculo')
    list_filter = ('tipo',)
    search_fields = ('nome',)
    inlines = [CompraInsumoInline]
    def preco_unitario_display(self, obj):
        return f"R$ {obj.preco_unitario:.2f}" if obj.preco_unitario else "-"
    preco_unitario_display.short_description = "Preço Unitário Atual"
