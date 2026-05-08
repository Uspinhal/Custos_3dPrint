from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome', 'whatsapp', 'instagram', 'email', 'documento',
            'tipo', 'estagio', 'origem', 'canal',
            'observacoes', 'ativo',
        ]
        widgets = {
            'nome':        forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '11999999999'}),
            'instagram':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'email':       forms.EmailInput(attrs={'class': 'form-control'}),
            'documento':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF ou CNPJ'}),
            'tipo':        forms.Select(attrs={'class': 'form-select'}),
            'estagio':     forms.Select(attrs={'class': 'form-select'}),
            'origem':      forms.Select(attrs={'class': 'form-select'}),
            'canal':       forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }