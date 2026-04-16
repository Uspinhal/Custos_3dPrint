from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Orcamento
from .forms import OrcamentoForm


def lista_orcamentos(request):
    orcamentos = Orcamento.objects.all()
    return render(request, 'precificacao/lista.html', {'orcamentos': orcamentos})


def criar_orcamento(request):
    # Permite pré-preencher custo_impressao vindo da tela de custos via GET
    custo_inicial = request.GET.get('custo_impressao')
    tipo_inicial  = request.GET.get('tipo_impressao')

    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Orçamento salvo com sucesso!")
            return redirect('precificacao:lista')
    else:
        initial = {}
        if custo_inicial:
            initial['custo_impressao'] = custo_inicial
        if tipo_inicial:
            initial['tipo_impressao'] = tipo_inicial
        form = OrcamentoForm(initial=initial)

    return render(request, 'precificacao/form.html', {'form': form, 'titulo': 'Novo Orçamento'})


def editar_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Orçamento atualizado com sucesso!")
            return redirect('precificacao:lista')
    else:
        form = OrcamentoForm(instance=orcamento)

    return render(request, 'precificacao/form.html', {'form': form, 'titulo': 'Editar Orçamento', 'orcamento': orcamento})


def detalhe_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    return render(request, 'precificacao/detalhe.html', {'orcamento': orcamento})


def deletar_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    orcamento.delete()
    messages.success(request, "Orçamento excluído.")
    return redirect('precificacao:lista')