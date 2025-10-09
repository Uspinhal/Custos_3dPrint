from django.db import models

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
    nome = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    custo_aquisicao = models.FloatField(default=0)
    custo_manutencao_mensal = models.FloatField(default=0)
    potencia_watts = models.FloatField(default=0)

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

    def __str__(self):
        return self.nome