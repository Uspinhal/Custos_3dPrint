from django.contrib import admin
from .models import Cliente

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'tipo', 'estagio', 'origem', 'canal', 'whatsapp', 'ativo', 'criado_em']
    list_filter   = ['tipo', 'estagio', 'origem', 'canal', 'ativo']
    search_fields = ['nome', 'whatsapp', 'instagram', 'email', 'documento']
    readonly_fields = ['criado_em', 'atualizado_em']

    fieldsets = [
        ('Identificação', {
            'fields': ['nome', 'whatsapp', 'instagram', 'email', 'documento']
        }),
        ('Classificação', {
            'fields': ['tipo', 'estagio', 'origem', 'canal']
        }),
        ('Notas', {
            'fields': ['observacoes', 'ativo']
        }),
        ('Metadados', {
            'fields': ['criado_em', 'atualizado_em'],
            'classes': ['collapse']
        }),
    ]