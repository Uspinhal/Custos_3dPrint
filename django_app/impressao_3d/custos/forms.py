from typing import Optional, cast
from django import forms
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima

class CalculoCustosForm(forms.Form):
    TIPO_CHOICES = [
        ('filamento', 'Filamento'), 
        ('resina', 'Resina')
        ]


    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label="Tipo de Impressão")
    # Evitar consulta no import; usar .none() e popular no __init__
    equipamento = forms.ModelChoiceField(queryset=Equipamento.objects.none(), label="Equipamento")
    materia_prima = forms.ModelChoiceField(queryset=MateriaPrima.objects.none(), label="Matéria Prima")
    quantidade = forms.FloatField(label="Quantidade (g)", min_value=0)
    tempo_horas = forms.FloatField(label="Tempo de Impressão (horas)", min_value=0)
    taxa_perda = forms.FloatField(label="Taxa de Perda (%)", min_value=0, max_value=100, initial=0.0, required=False)

    def __init__(self, *args, tipo: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # popular queryset do equipamento (evita consulta no import)
        field = cast(forms.ModelChoiceField, self.fields['equipamento'])
        field.queryset = Equipamento.objects.all()

        # escolher queryset das materias, filtrando por tipo se informado
        if tipo:
            qs = MateriaPrima.objects.filter(tipo=tipo)
        else:
            qs = MateriaPrima.objects.all()

        # informa o type checker que é um ModelChoiceField antes de atribuir .queryset
        field = cast(forms.ModelChoiceField, self.fields['materia_prima'])
        field.queryset = qs