from django.db import models

# Create your models here.

class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nome

class MateriaPrima(models.Model):
    TIPOS = [
        ('filamento', 'Filamento'),
        ('resina', 'Resina'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, blank=True, null=True)
    material = models.CharField(max_length=30, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="materias_primas", blank=True, null=True)
    quantidade = models.FloatField()
    estoque_minimo = models.FloatField(default=0)
    preco = models.FloatField()

    class Meta:
        verbose_name = "Matéria Prima"
        verbose_name_plural = "Matérias Primas"

    def __str__(self):
        return self.nome

class Insumos(models.Model):
    TIPO_INSUMO = [
                ('consumivel', 'Consumível'),
                ('protecao', 'Proteção'),
                ('manutencao', 'Manutenção'),
                ('energia', 'Energia'),
                ('outros', 'Outros'),
    ]


    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_INSUMO, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.FloatField()
    unidade = models.CharField(max_length=20, default='unidade', help_text="Ex: g, kg, ml, kWh")
    estoque_minimo = models.FloatField(default=0)
    preco_unitario = models.FloatField()
    quantidade_minima = models.FloatField(default=0)
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    def __str__(self):
        return self.nome