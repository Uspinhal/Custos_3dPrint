from django.db import models
from django.utils import timezone


# ---------------------------------------------------------------------------
# Pedido
# ---------------------------------------------------------------------------

class Pedido(models.Model):
    ORIGEM_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("yampi",    "Yampi"),
        ("loja",     "Loja"),
    ]
    PRIORIDADE_CHOICES = [
        ("normal",  "Normal"),
        ("urgente", "Urgente"),
    ]

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="pedidos",
        verbose_name="Cliente",
    )
    orcamento = models.ForeignKey(
        "precificacao.Orcamento",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="pedidos",
        verbose_name="Orçamento",
    )

    origem    = models.CharField(max_length=20, choices=ORIGEM_CHOICES, verbose_name="Origem")
    referencia_yampi = models.CharField(
        max_length=100, blank=True,
        verbose_name="Referência Yampi",
        help_text="Número do pedido na Yampi (preenchido manualmente).",
    )
    prioridade = models.CharField(
        max_length=20, choices=PRIORIDADE_CHOICES,
        default="normal", verbose_name="Prioridade",
    )

    is_enviado = models.BooleanField(
        default=False,
        verbose_name="Enviado",
        help_text="Marcar apenas após confirmação de postagem. Único status manual.",
    )

    data_pedido = models.DateField(default=timezone.now, verbose_name="Data do pedido")
    data_prazo  = models.DateField(null=True, blank=True, verbose_name="Prazo")
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-data_pedido", "-prioridade"]

    def __str__(self):
        cliente_str = str(self.cliente) if self.cliente else "Sem cliente"
        return f"Pedido #{self.pk} — {cliente_str}"

    STATUS_NA_FILA     = "na_fila"
    STATUS_EM_PRODUCAO = "em_producao"
    STATUS_EMBALADO    = "embalado"
    STATUS_ENVIADO     = "enviado"

    STATUS_LABELS = {
        STATUS_NA_FILA:     "Na fila",
        STATUS_EM_PRODUCAO: "Em produção",
        STATUS_EMBALADO:    "Embalado",
        STATUS_ENVIADO:     "Enviado",
    }

    @property
    def status(self):
        if self.is_enviado:
            return self.STATUS_ENVIADO

        itens = list(self.itens.all())  # type: ignore[attr-defined]
        if not itens:
            return self.STATUS_NA_FILA

        statuses = [item.status for item in itens]

        if all(s == "concluido" for s in statuses):
            return self.STATUS_EMBALADO

        if any(s == "imprimindo" for s in statuses):
            return self.STATUS_EM_PRODUCAO

        return self.STATUS_NA_FILA

    @property
    def status_display(self):
        return self.STATUS_LABELS.get(self.status, self.status)


# ---------------------------------------------------------------------------
# ItemPedido
# ---------------------------------------------------------------------------

class ItemPedido(models.Model):
    TIPO_IMPRESSAO_CHOICES = [
        ("resina",    "Resina"),
        ("filamento", "Filamento"),
    ]

    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        related_name="itens", verbose_name="Pedido",
    )
    descricao      = models.CharField(max_length=255, verbose_name="Descrição")
    quantidade     = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    tipo_impressao = models.CharField(
        max_length=20, choices=TIPO_IMPRESSAO_CHOICES,
        verbose_name="Tipo de impressão",
    )
    arquivo_stl = models.CharField(
        max_length=255, blank=True,
        verbose_name="Arquivo STL",
        help_text="Nome do arquivo. Ex: goblin_archer_v2.stl",
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.descricao} (x{self.quantidade}) — Pedido #{self.pedido_id}" # type: ignore[attr-defined]

    @property
    def status(self):
        ultimo = (
            self.op_itens  # type: ignore[attr-defined]
            .select_related("ordem")
            .order_by("-ordem__id")
            .first()
        )
        return ultimo.status if ultimo else "na_fila"

    @property
    def status_display(self):
        labels = {
            "na_fila":    "Na fila",
            "imprimindo": "Imprimindo",
            "concluido":  "Concluído",
            "falhou":     "Falhou",
        }
        return labels.get(self.status, self.status)


# ---------------------------------------------------------------------------
# OrdemProducao
# ---------------------------------------------------------------------------

class OrdemProducao(models.Model):
    impressora = models.ForeignKey(
        "equipamentos.Equipamento",
        on_delete=models.PROTECT,
        related_name="ordens_producao",
        verbose_name="Impressora",
    )
    materia_prima = models.ForeignKey(
        "estoque.MateriaPrima",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="ordens",
        verbose_name="Matéria-Prima",
    )
    quantidade_utilizada = models.FloatField(
        null=True, blank=True,
        verbose_name="Quantidade utilizada (g ou ml)",
        help_text=(
            "Obrigatório para fechar a OP. "
            "Validado na view na transição de status → concluida."
        ),
    )
    data_inicio    = models.DateTimeField(null=True, blank=True, verbose_name="Início")
    data_conclusao = models.DateTimeField(null=True, blank=True, verbose_name="Conclusão")
    observacoes    = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Ordem de Produção"
        verbose_name_plural = "Ordens de Produção"
        ordering = ["-id"]

    def __str__(self):
        return f"OP #{self.pk:03d}"

    STATUS_AGENDADA            = "agendada"
    STATUS_IMPRIMINDO          = "imprimindo"
    STATUS_PARCIALMENTE_FALHOU = "parcialmente_falhou"
    STATUS_AGUARDANDO_FINALIZACAO = "aguardando_finalizacao"
    STATUS_CONCLUIDA           = "concluida"

    STATUS_LABELS = {
        STATUS_AGENDADA:            "Agendada",
        STATUS_IMPRIMINDO:          "Imprimindo",
        STATUS_PARCIALMENTE_FALHOU: "Parcialmente falhou",
        STATUS_AGUARDANDO_FINALIZACAO: "Aguardando finalização",
        STATUS_CONCLUIDA:           "Concluída",
    }

    @property
    def status(self):
        statuses = list(self.op_itens.values_list("status", flat=True))  # type: ignore[attr-defined]

        if self.data_conclusao:
            return self.STATUS_CONCLUIDA

        if not statuses:
            return self.STATUS_AGENDADA

        if all(s == "concluido" for s in statuses):
            return self.STATUS_AGUARDANDO_FINALIZACAO

        if any(s == "imprimindo" for s in statuses):
            return self.STATUS_IMPRIMINDO

        if any(s == "falhou" for s in statuses):
            return self.STATUS_PARCIALMENTE_FALHOU

        return self.STATUS_AGENDADA

    @property
    def status_display(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def numero_arquivo(self):
        if self.pk is None:
            return "-"
        return f"OP{self.pk:03d}"


# ---------------------------------------------------------------------------
# OrdemProducaoItem
# ---------------------------------------------------------------------------

class OrdemProducaoItem(models.Model):
    STATUS_CHOICES = [
        ("na_fila",    "Na fila"),
        ("imprimindo", "Imprimindo"),
        ("concluido",  "Concluído"),
        ("falhou",     "Falhou"),
    ]

    ordem = models.ForeignKey(
        OrdemProducao, on_delete=models.CASCADE,
        related_name="op_itens", verbose_name="Ordem de Produção",
    )
    item = models.ForeignKey(
        ItemPedido, on_delete=models.CASCADE,
        related_name="op_itens", verbose_name="Item do Pedido",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default="na_fila", verbose_name="Status",
    )

    class Meta:
        verbose_name = "Item da Ordem de Produção"
        verbose_name_plural = "Itens da Ordem de Produção"
        unique_together = [("ordem", "item")]

    def __str__(self):
        return (
            f"OP #{self.ordem_id:03d} → " # type: ignore[attr-defined]
            f"{self.item.descricao} [{self.get_status_display()}]"  # type: ignore[attr-defined]
        )
