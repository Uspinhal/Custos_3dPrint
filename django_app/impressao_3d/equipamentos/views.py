from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipamento, Fabricante
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from .forms import EquipamentoForm
import json




# Create your views here.
def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all().order_by('nome')
    print("Equipamentos no view:", equipamentos) 
    return render(request, 'equipamentos/lista.html', {'equipamentos': equipamentos})

def criar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipamentos:lista')
    else:
        form = EquipamentoForm()
    return render(request, 'equipamentos/form.html', {'form': form, 'fabricantes': Fabricante.objects.all()})


def editar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('equipamentos:lista')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'equipamentos/form.html', {'form': form, 'fabricantes': Fabricante.objects.all(), 'equipamento': equipamento})


def deletar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    equipamento.delete()
    return redirect('equipamentos:lista')


def adicionar_fabricante_ajax(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        if not nome:
            return JsonResponse({'error': 'Nome é obrigatório.'}, status=400)
        
        fabricante, created = Fabricante.objects.get_or_create(nome=nome)
        return JsonResponse({'id': fabricante.id, 'nome': fabricante.nome}) if created else JsonResponse({'error': 'Fabricante já existe.'}, status=400) # type: ignore

    return JsonResponse({'error': 'Método não permitido.'}, status=405)

