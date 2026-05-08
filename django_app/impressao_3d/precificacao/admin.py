from django.contrib import admin
from .models import Orcamento

# Register your models here.

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display  = ['referencia', 'descricao', 'cliente', 'status', 'preco_final', 'data_criacao']
    list_filter   = ['status', 'tipo_impressao']
    search_fields = ['descricao', 'cliente_nome']
    readonly_fields = ['referencia', 'custo_base', 'preco_final']