from django.db import models

# Create your models here.
class Cliente(models.Model):

    class Tipo(models.TextChoices):
        B2C = 'B2C', 'Pessoa Física'
        B2B = 'B2B', 'Pessoa Jurídica / Revendedor'

    class Estagio(models.TextChoices):
        LEAD       = 'lead',       'Lead'
        PRIMEIRO   = 'primeiro',   'Primeiro Pedido'
        RECORRENTE = 'recorrente', 'Recorrente'
        INATIVO    = 'inativo',    'Inativo'
        VIP        = 'vip',        'VIP'

    class Origem(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        TIKTOK    = 'tiktok',    'TikTok'
        FACEBOOK  = 'facebook',  'Facebook'
        DISCORD   = 'discord',   'Discord / Comunidade'
        INDICACAO = 'indicacao', 'Indicação'
        ORGANICO  = 'organico',  'Busca Orgânica'
        OUTRO     = 'outro',     'Outro'

    class Canal(models.TextChoices):
        WHATSAPP   = 'whatsapp',   'WhatsApp'
        DM_INSTA   = 'dm_insta',   'DM Instagram'
        DM_FACE    = 'dm_face',    'DM Facebook'
        EMAIL      = 'email',      'Email'
        PRESENCIAL = 'presencial', 'Presencial'

    # Identificação
    nome      = models.CharField(max_length=200)
    whatsapp  = models.CharField(max_length=20, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    email     = models.EmailField(blank=True)
    documento = models.CharField(
        max_length=18, blank=True,
        verbose_name='CPF / CNPJ',
        help_text='Opcional — CPF (000.000.000-00) ou CNPJ (00.000.000/0000-00)'
    )

    # Classificação
    tipo    = models.CharField(max_length=3,  choices=Tipo.choices,    default=Tipo.B2C)
    estagio = models.CharField(max_length=20, choices=Estagio.choices, default=Estagio.LEAD)
    origem  = models.CharField(max_length=20, choices=Origem.choices,  blank=True)
    canal   = models.CharField(max_length=20, choices=Canal.choices,   blank=True)

    # Notas
    observacoes   = models.TextField(blank=True)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo         = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} [{self.get_tipo_display()} — {self.get_estagio_display()}]" # type: ignore