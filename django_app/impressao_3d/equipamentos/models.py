from django.db import models
from datetime import date

# Create your models here.
class Fabricante(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Fabricante"
        verbose_name_plural = "Fabricantes"

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    TIPO_EQUIPAMENTO = [
        ('Filamento', 'Filamento'),
        ('Resina', 'Resina'),
        ('Wash & Cure', 'Wash & Cure'),
        ('Outros', 'Outros'),
    ]
    nome = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_EQUIPAMENTO, blank=True, null=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    custo_aquisicao = models.FloatField(default=0)
    custo_manutencao_mensal = models.FloatField(default=0)
    potencia_watts = models.FloatField(default=0)
    vida_util_anos = models.IntegerField(default=5) # Vida útil em anos
    valor_residual = models.FloatField(default=0)
    observacoes = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return self.nome
    
    def calcular_valor_residual(self):
        """Calcula o valor residual baseado na vida útil e custo de aquisição"""
        if not self.data_aquisicao or self.vida_util_anos <= 0:
            return self.custo_aquisicao

        anos_de_uso = (date.today() - self.data_aquisicao).days / 365
        depreciacao_total = (self.custo_aquisicao / self.vida_util_anos) * anos_de_uso
        valor_atual = self.custo_aquisicao - depreciacao_total

        # Evita valor negativo
        return round(max(valor_atual, 0), 2)
    

    def save(self, *args, **kwargs):
        # Atualiza automaticamente o valor_residual ao salvar
        self.valor_residual = self.calcular_valor_residual()
        self.custo_manutencao_mensal = self.custo_manutencao()
        super().save(*args, **kwargs)

    def custo_manutencao(self):
        """Calcula o custo total de manutenção para um número dado de meses"""
        if self.tipo == 'Resina':
            self.custo_manutencao_mensal = self.custo_aquisicao/2000  # Custo fixo mensal para equipamentos de resina
        return round(max(self.custo_manutencao_mensal, 0), 2)
