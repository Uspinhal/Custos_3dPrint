from django import forms
from .models import Orcamento


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            'descricao',
            'tipo_impressao',
            'custo_impressao',
            'custo_modelagem',
            'outros_custos',
            'margem_lucro',
            'taxa_plataforma',
            'taxa_cartao',
            'status',
            'observacoes',
        ]
        widgets = {
            'descricao':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Miniatura Guerreiro 32mm'}),
            'tipo_impressao':  forms.Select(attrs={'class': 'form-select'}),
            'custo_impressao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'custo_modelagem': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'outros_custos':   forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'margem_lucro':    forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'taxa_plataforma': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'taxa_cartao':     forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'observacoes':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'descricao':       'Descrição do produto',
            'tipo_impressao':  'Tipo de impressão',
            'custo_impressao': 'Custo de impressão (R$)',
            'custo_modelagem': 'Modelagem / Arquivo STL (R$)',
            'outros_custos':   'Outros custos (R$)',
            'margem_lucro':    'Margem de lucro (%)',
            'taxa_plataforma': 'Taxa da plataforma (%)',
            'taxa_cartao':     'Taxa do cartão (%)',
            'status':          'Status',
            'observacoes':     'Observações',
        }
        help_texts = {
            'custo_impressao': 'Cole aqui o valor calculado na tela de Calcular Custo.',
            'custo_modelagem': 'Deixe 0 se não houver custo de modelagem ou STL.',
            'taxa_plataforma': 'Padrão: 2,5% (Yampi). Altere se necessário.',
            'taxa_cartao':     'Padrão: 3,99%. Altere se necessário.',
        }