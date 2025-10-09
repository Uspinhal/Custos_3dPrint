from django.db import models

# Create your models here.
class MateriaPrima(models.Model):
    TIPOS = [
        ('filamento', 'Filamento'),
        ('resina', 'Resina'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, blank=True, null=True)
    material = models.CharField(max_length=30, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    quantidade = models.FloatField()
    estoque_minimo = models.FloatField(default=0)
    preco = models.FloatField()

    class Meta:
        verbose_name = "Matéria Prima"
        verbose_name_plural = "Matérias Primas"

    def __str__(self):
        return self.nome