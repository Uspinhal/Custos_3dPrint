from django import forms
from .models import Equipamento, Fabricante

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = [
            "nome", "modelo", "tipo", "fabricante", "data_aquisicao",
            "custo_aquisicao", "custo_manutencao_mensal",
            "potencia_watts", "vida_util_anos"
        ]
        widgets = {
            "data_aquisicao": forms.DateInput(attrs={"type": "date"}),
        }
