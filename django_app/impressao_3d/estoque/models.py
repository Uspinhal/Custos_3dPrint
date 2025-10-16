from __future__ import annotations
from typing import Any
from django.utils.timezone import now as tz_now
from time import timezone
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
    quantidade = models.FloatField(help_text="Quantidade total comprada (em kg, L etc.)")
    estoque_minimo = models.FloatField(default=0)
    preco_total = models.FloatField(default=0, help_text="Preço total pago na compra (R$)")
    preco_unitario = models.FloatField(editable=False, default=0, help_text="Preço por unidade (R$/kg, R$/L, etc.)")
    unidade = models.CharField(max_length=20, default='kg', help_text="Ex: kg, L, g, mL")

    def atualizar_preco_unitario(self):
        """
        Atualiza preco_unitario com base na última compra.
        Usa getattr para evitar aviso do analisador estático.
        """
        compras_manager = getattr(self, "compras", None)
        if compras_manager is None:
            return
        ultima_compra = compras_manager.order_by('-data_compra').first()
        
        if ultima_compra:
            self.preco_unitario = ultima_compra.preco_unitario()
            # salva sem recalcular o próprio preco_unitario (já calculado)
            super(MateriaPrima, self).save(update_fields=['preco_unitario'])

    class Meta:
        verbose_name = "Matéria Prima"
        verbose_name_plural = "Matérias Primas"

    def save(self, *args, **kwargs):
        if self.quantidade > 0:
            self.preco_unitario = self.preco_total / self.quantidade
        else:
            self.preco_unitario = 0
        super().save(*args, **kwargs)

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
    TIPOS_USO = [
                ('resina', 'Impressão com Resina'),
                ('filamento', 'Impressão com Filamento'),
                ('geral', 'Uso Geral'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=TIPO_INSUMO, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_USO, blank=False, null=True )
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.FloatField(help_text="Quantidade total comprada (em unidades, kg, L etc.)")
    unidade = models.CharField(max_length=20, default='unidade', help_text="Ex: g, kg, ml, kWh")
    estoque_minimo = models.FloatField(default=0)

    preco_total = models.FloatField(default=0, help_text="Preço total pago na compra (R$)")
    preco_unitario = models.FloatField(editable=False, default=0, help_text="Preço por unidade (R$/unidade, R$/kg, R$/L, etc.)")
    peso_no_calculo = models.FloatField(default=1)
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
    
    def save(self, *args, **kwargs):
        """Calcula automaticamente o preço unitário"""
        if self.quantidade > 0:
            self.preco_unitario = self.preco_total / self.quantidade
        else:
            self.preco_unitario = 0
        super().save(*args, **kwargs)
    
    def atualizar_preco_unitario(self):
        """Atualiza o preço unitário com base na última compra registrada."""
        compras_manager = getattr(self, "compras", None)
        if not compras_manager:
            return
        ultima_compra = compras_manager.order_by("-data_compra").first()
        if ultima_compra:
            self.preco_unitario = ultima_compra.preco_unitario()
            super(Insumos, self).save(update_fields=["preco_unitario"])

    def __str__(self):
        return self.nome
    

    
class CompraMateriaPrima(models.Model):
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, related_name="compras")
    data_compra = models.DateField(default=tz_now)
    quantidade = models.FloatField(help_text="Quantidade comprada (ex: 5 kg)")
    preco_total = models.FloatField(help_text="Preço total da compra")

    class Meta:
        verbose_name = "Compra Matéria-prima"
        verbose_name_plural = "Compras Matérias-primas"

    def preco_unitario(self) -> float:
        return (self.preco_total / self.quantidade) if self.quantidade and self.quantidade > 0 else 0.0

    def __str__(self) -> str:
        return f"{self.materia_prima.nome} - {self.data_compra.strftime('%d/%m/%Y')}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        # salva a compra, depois atualiza o preco unitário do material
        super().save(*args, **kwargs)
        # atualiza o preco_unitario do objeto relacionado
        try:
            self.materia_prima.atualizar_preco_unitario()
        except Exception:
            # evita que erros de atualização quebrem o save (logue se quiser)
            pass

class CompraInsumo(models.Model):
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE, related_name="compras")
    data_compra = models.DateField(default=tz_now)
    quantidade = models.FloatField(help_text="Quantidade comprada (ex: 5 kg, 3 L)")
    preco_total = models.FloatField(help_text="Preço total da compra")

    class Meta:
        verbose_name = "Compra de Insumo"
        verbose_name_plural = "Compras de Insumos"

    def preco_unitario(self):
        return (self.preco_total / self.quantidade) if self.quantidade and self.quantidade > 0 else 0.0

    def __str__(self):
        return f"{self.insumo.nome} - {self.data_compra.strftime('%d/%m/%Y')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.insumo.atualizar_preco_unitario()
        except Exception:
            pass