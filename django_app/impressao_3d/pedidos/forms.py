from django import forms
from clientes.models import Cliente
from precificacao.models import Orcamento
from .models import Pedido, ItemPedido, OrdemProducao, OrdemProducaoItem


# ---------------------------------------------------------------------------
# Pedido
# ---------------------------------------------------------------------------

class PedidoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(ativo=True).order_by('nome'),
        required=False,
        empty_label='— Sem cliente —',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    orcamento = forms.ModelChoiceField(
        queryset=Orcamento.objects.order_by('-data_criacao'),
        required=False,
        empty_label='— Sem orçamento —',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Pedido
        fields = [
            'cliente', 'orcamento', 'origem', 'referencia_yampi',
            'prioridade', 'data_pedido', 'data_prazo', 'observacoes',
        ]
        widgets = {
            'origem':          forms.Select(attrs={'class': 'form-select'}),
            'referencia_yampi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1234'}),
            'prioridade':      forms.Select(attrs={'class': 'form-select'}),
            'data_pedido':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_prazo':      forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'observacoes':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ---------------------------------------------------------------------------
# ItemPedido  (usado no inlineformset)
# ---------------------------------------------------------------------------

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['descricao', 'quantidade', 'tipo_impressao', 'arquivo_stl', 'observacoes']
        widgets = {
            'descricao':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Goblin Archer 32mm'}),
            'quantidade':     forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'tipo_impressao': forms.Select(attrs={'class': 'form-select'}),
            'arquivo_stl':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: goblin_archer_v2.stl'}),
            'observacoes':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ---------------------------------------------------------------------------
# OrdemProducao
# ---------------------------------------------------------------------------

class OrdemProducaoForm(forms.ModelForm):
    class Meta:
        model = OrdemProducao
        fields = [
            'impressora', 'materia_prima', 'data_inicio', 'observacoes',
        ]
        widgets = {
            'impressora':           forms.Select(attrs={'class': 'form-select'}),
            'materia_prima':        forms.Select(attrs={'class': 'form-select'}),
            'data_inicio':          forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'observacoes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'impressora':           'Impressora',
            'materia_prima':        'Matéria-Prima',
            'data_inicio':          'Início',
            'observacoes':          'Observações',
        }


# ---------------------------------------------------------------------------
# OrdemProducaoItem — só o status, usado no detalhe da OP
# ---------------------------------------------------------------------------

class OrdemProducaoItemStatusForm(forms.ModelForm):
    class Meta:
        model = OrdemProducaoItem
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
