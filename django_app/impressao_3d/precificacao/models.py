from django.db import models
from django.utils.timezone import now as tz_now


class Orcamento(models.Model):

    STATUS_CHOICES = [
        ('rascunho',  'Rascunho'),
        ('enviado',   'Enviado'),
        ('aprovado',  'Aprovado'),
        ('recusado',  'Recusado'),
    ]

    TIPO_IMPRESSAO = [
        ('resina',    'Resina'),
        ('filamento', 'Filamento'),
    ]

    # Identificação
    descricao       = models.CharField(max_length=200, help_text="Ex: Miniatura Guerreiro 32mm")
    data_criacao    = models.DateField(default=tz_now)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')

    # Tipo de impressão (para referência)
    tipo_impressao  = models.CharField(max_length=20, choices=TIPO_IMPRESSAO, blank=True, null=True)

    # Custos vindos do módulo de custos
    custo_impressao = models.FloatField(help_text="Custo total calculado pelo módulo de custos (R$)")

    # Custos extras (opcionais)
    custo_modelagem = models.FloatField(default=0, help_text="Custo de modelagem 3D ou compra de arquivo STL (R$)")
    outros_custos   = models.FloatField(default=0, help_text="Outros custos diretos (R$)")

    # Precificação
    margem_lucro    = models.FloatField(default=40.0, help_text="Margem de lucro desejada (%)")

    # Taxas fixas (armazenadas para histórico, caso mudem no futuro)
    taxa_plataforma = models.FloatField(default=2.5,  help_text="Taxa da plataforma de vendas (%)")
    taxa_cartao     = models.FloatField(default=3.99, help_text="Taxa da administradora de cartão (%)")

    # Resultado calculado (salvo para histórico)
    custo_base      = models.FloatField(default=0, help_text="Soma de todos os custos antes da margem (R$)")
    preco_final     = models.FloatField(default=0, help_text="Preço de venda calculado (R$)")

    # Observações
    observacoes     = models.TextField(blank=True, null=True)

    # Contato do cliente (temporário até módulo de clientes)
    cliente_nome     = models.CharField(max_length=100, blank=True, null=True, help_text="Nome do cliente")
    cliente_telefone = models.CharField(max_length=20, blank=True, null=True, help_text="Ex: 11999999999 (só números)")

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ['-data_criacao']

    def calcular(self):
        """Calcula custo_base e preco_final e atualiza os campos."""
        self.custo_base = round(
            self.custo_impressao + self.custo_modelagem + self.outros_custos, 2
        )

        # Taxas e margem incidem sobre o preço final (cálculo de trás pra frente)
        divisor = 1 - (self.margem_lucro / 100) - (self.taxa_plataforma / 100) - (self.taxa_cartao / 100)

        if divisor <= 0:
            # Margem + taxas >= 100% — inviável
            self.preco_final = 0
        else:
            self.preco_final = round(self.custo_base / divisor, 2)

    def save(self, *args, **kwargs):
        self.calcular()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descricao} — R$ {self.preco_final:.2f} ({self.get_status_display()})" #type: ignore