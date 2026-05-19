from django.contrib import admin
from .models import Pedido, ItemPedido, OrdemProducao, OrdemProducaoItem


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    fields = ["descricao", "quantidade", "tipo_impressao", "arquivo_stl", "observacoes"]
    show_change_link = True


class OrdemProducaoItemInline(admin.TabularInline):
    model = OrdemProducaoItem
    extra = 1
    fields = ["item", "status"]
    autocomplete_fields = ["item"]


# ---------------------------------------------------------------------------
# Pedido
# ---------------------------------------------------------------------------

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display  = ["id", "cliente", "origem", "prioridade", "status_display", "data_pedido", "data_prazo", "is_enviado"]
    list_filter   = ["origem", "prioridade", "is_enviado"]
    search_fields = ["cliente__nome", "referencia_yampi", "observacoes"]
    readonly_fields = ["status_display"]
    autocomplete_fields = ["cliente", "orcamento"]
    inlines = [ItemPedidoInline]

    fieldsets = [
        ("Identificação", {
            "fields": ["cliente", "orcamento", "origem", "referencia_yampi"]
        }),
        ("Produção", {
            "fields": ["prioridade", "data_pedido", "data_prazo", "is_enviado", "status_display"]
        }),
        ("Observações", {
            "fields": ["observacoes"]
        }),
    ]

    @admin.display(description="Status")
    def status_display(self, obj):
        return obj.status_display  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# ItemPedido  (acesso direto para busca via autocomplete no inline da OP)
# ---------------------------------------------------------------------------

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display  = ["descricao", "pedido", "quantidade", "tipo_impressao", "status_display"]
    list_filter   = ["tipo_impressao"]
    search_fields = ["descricao", "pedido__cliente__nome"]
    readonly_fields = ["status_display"]

    @admin.display(description="Status")
    def status_display(self, obj):
        return obj.status_display  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# OrdemProducao
# ---------------------------------------------------------------------------

@admin.register(OrdemProducao)
class OrdemProducaoAdmin(admin.ModelAdmin):
    list_display  = ["__str__", "impressora", "materia_prima", "status_display", "quantidade_utilizada", "data_inicio", "data_conclusao"]
    list_filter   = ["impressora", "materia_prima"]
    search_fields = ["observacoes"]
    readonly_fields = ["status_display", "numero_arquivo"]
    inlines = [OrdemProducaoItemInline]

    fieldsets = [
        ("Configuração", {
            "fields": ["impressora", "materia_prima", "quantidade_utilizada"]
        }),
        ("Datas", {
            "fields": ["data_inicio", "data_conclusao"]
        }),
        ("Info", {
            "fields": ["status_display", "numero_arquivo", "observacoes"]
        }),
    ]

    @admin.display(description="Status")
    def status_display(self, obj):
        return obj.status_display  # type: ignore[attr-defined]