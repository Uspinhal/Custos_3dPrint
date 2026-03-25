import re
from typing import Optional, cast
from django import forms
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima

class TempoImpressaoField(forms.CharField):
    """Campo que aceita tempo no formato H:MM ou HH:MM (como o fatiador exporta)
    e converte internamente para horas decimais (float).
 
    Exemplos:
        "2:30"  → 2.5
        "0:45"  → 0.75
        "1:05"  → 1.0833...
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Tempo de Impressão (H:MM)')
        kwargs.setdefault("widget", forms.TextInput(attrs={'placeholder': 'Ex: 2:30',"type": "text"}))
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value) # lida com required/empty
        if not value:
            return None
        value = value.strip()

        # Aceita tanto "2:30" quanto "2h30" ou "2h 30m" (formatos comuns de fatiadores)
        match = re.fullmatch(r"(\d{1,3})[h:]\s*(\d{1,2})m?", value, re.IGNORECASE)
        if match:
            horas = int(match.group(1))
            minutos = int(match.group(2))
            if minutos >= 60:
                raise forms.ValidationError("Minutos devem ser entre 0 e 59.")
            return horas + minutos / 60
        
        # Também aceita número decimal puro ("2.5") para flexibilidade
        try:
            decimal = float(value.replace(',', '.')) # aceita vírgula como separador decimal
            if decimal < 0:
                raise forms.ValidationError("Tempo não pode ser negativo.")
            return decimal
        except ValueError:
            pass

        raise forms.ValidationError("Formato inválido. Use H:MM ou número decimal (ex: 2:30 ou 2.5).")



class CalculoCustosForm(forms.Form):
    TIPO_CHOICES = [
        ('selecione','SELECIONE'),
        ('filamento', 'Filamento'), 
        ('resina', 'Resina')
        ]


    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label="Tipo de Impressão")
    # Evitar consulta no import; usar .none() e popular no __init__
    equipamento = forms.ModelChoiceField(queryset=Equipamento.objects.none(), label="Equipamento")
    materia_prima = forms.ModelChoiceField(queryset=MateriaPrima.objects.none(), label="Matéria Prima")
    quantidade = forms.FloatField(label="Quantidade (g)", min_value=0)
    tempo_horas = TempoImpressaoField()
    taxa_perda = forms.FloatField(label="Taxa de Perda (%)", min_value=0, max_value=100, initial=0.0, required=False)

    def __init__(self, *args, tipo: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)

        # Mapeamento: valor do choice (minúsculo) → valor do campo tipo em Equipamento (capitalizado)
        TIPO_EQUIPAMENTO_MAP = {
            "resina": "Resina",
            "filamento": "Filamento",
        }
        
        eq_field = cast(forms.ModelChoiceField, self.fields["equipamento"])
        if tipo and tipo in TIPO_EQUIPAMENTO_MAP:
            eq_field.queryset = Equipamento.objects.filter(tipo=TIPO_EQUIPAMENTO_MAP[tipo]).order_by("nome")
        else:
            eq_field.queryset = Equipamento.objects.all().order_by("nome")

        mp_field = cast(forms.ModelChoiceField, self.fields["materia_prima"])
        if tipo and tipo in TIPO_EQUIPAMENTO_MAP:
            mp_field.queryset = MateriaPrima.objects.filter(tipo=tipo).order_by("nome")
        else:
            mp_field.queryset = MateriaPrima.objects.all().order_by("nome")
        