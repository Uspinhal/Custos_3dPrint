from django.shortcuts import render, redirect, get_object_or_404
from .models import MateriaPrima, Marca, Insumos, CompraInsumo, CompraMateriaPrima
from .forms import MateriaPrimaForm, InsumoForm

# ----------- MATÉRIAS-PRIMAS -----------

def lista_materias_primas(request):
    materias = MateriaPrima.objects.all().order_by('nome')
    return render(request, 'materias_primas/lista.html', {'materias': materias})

def criar_materia_prima(request):
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque:lista_materias_primas')
    else:
        form = MateriaPrimaForm()
    return render(request, 'materias_primas/form.html', {'form': form})


def editar_materia_prima(request, materia_id):
    materia = get_object_or_404(MateriaPrima, id=materia_id)
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('estoque:lista_materias_primas')
    else:
        form = MateriaPrimaForm(instance=materia)
    return render(request, 'materias_primas/form.html', {'form': form, 'materia': materia})

def deletar_materia_prima(request, materia_id):
    materia = get_object_or_404(MateriaPrima, id=materia_id)
    materia.delete()
    return redirect('estoque:lista_materias_primas')


# ----------- INSUMOS -----------

def lista_insumos(request):
    insumos = Insumos.objects.all().order_by('nome')
    return render(request, 'insumos/lista.html', {'insumos': insumos})

def criar_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque:lista_insumos')        
    else:
        form = InsumoForm()
    return render(request, 'insumos/form.html', {'form': form})


def editar_insumo(request, insumo_id):
    insumo = get_object_or_404(Insumos, id=insumo_id)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            return redirect('estoque:lista_insumos')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'insumos/form.html', {'form': form, 'insumo': insumo})

def deletar_insumo(request, insumo_id):
    insumo = get_object_or_404(Insumos, id=insumo_id)
    insumo.delete()
    return redirect('estoque:lista_insumos')

# -------------------- Compras Matéria-Prima --------------------
def lista_compras_materia(request, materia_id=None):
    if materia_id:
        compras = CompraMateriaPrima.objects.filter(materia_prima_id=materia_id).order_by('-data_compra')
    else:
        compras = CompraMateriaPrima.objects.all().order_by('-data_compra')
    return render(request, 'materias_primas/compras_lista.html', {'compras': compras})

def criar_compra_materia(request, materia_id=None):
    materias = MateriaPrima.objects.all().order_by('nome')
    if request.method == 'POST':
        materia_prima_id = request.POST.get('materia_prima')
        quantidade = float(request.POST.get('quantidade', 0))
        preco_total = float(request.POST.get('preco_total', 0))
        data_compra = request.POST.get('data_compra') or None

        materia = MateriaPrima.objects.get(id=materia_prima_id)
        CompraMateriaPrima.objects.create(
            materia_prima=materia,
            quantidade=quantidade,
            preco_total=preco_total,
            data_compra=data_compra
        )
        return redirect('estoque:lista_compras_materia')

    return render(request, 'materias_primas/compras_form.html', {'materias': materias})
def editar_compra_materia(request, compra_id):
    compra = get_object_or_404(CompraMateriaPrima, id=compra_id)
    materias = MateriaPrima.objects.all().order_by('nome')

    if request.method == 'POST':
        materia_id = int(request.POST.get('materia_prima'))
        compra.materia_prima = MateriaPrima.objects.get(id=materia_id)
        compra.quantidade = float(request.POST.get('quantidade', 0))
        compra.preco_total = float(request.POST.get('preco_total', 0))
        compra.data_compra = request.POST.get('data_compra') or compra.data_compra
        compra.save()
        return redirect('estoque:lista_compras_materia')

    return render(request, 'materias_primas/compras_form.html', {'compra': compra, 'materias': materias})

def deletar_compra_materia(request, compra_id):
    compra = get_object_or_404(CompraMateriaPrima, id=compra_id)
    compra.delete()
    return redirect('estoque:lista_compras_materia')

# -------------------- Compras Insumos --------------------
def lista_compras_insumo(request, insumo_id=None):
    if insumo_id:
        compras = CompraInsumo.objects.filter(insumo_id=insumo_id).order_by('-data_compra')
    else:
        compras = CompraInsumo.objects.all().order_by('-data_compra')
    return render(request, 'insumos/compras_lista.html', {'compras': compras})

def criar_compra_insumo(request, insumo_id=None):
    insumos = Insumos.objects.all().order_by('nome')
    if request.method == 'POST':
        insumo_id = request.POST.get('insumo')
        quantidade = float(request.POST.get('quantidade', 0))
        preco_total = float(request.POST.get('preco_total', 0))
        data_compra = request.POST.get('data_compra') or None

        insumo = Insumos.objects.get(id=insumo_id)
        CompraInsumo.objects.create(
            insumo=insumo,
            quantidade=quantidade,
            preco_total=preco_total,
            data_compra=data_compra
        )
        return redirect('estoque:lista_compras_insumo')

    return render(request, 'insumos/compras_form.html', {'insumos': insumos})
def editar_compra_insumo(request, compra_id):
    compra = get_object_or_404(CompraInsumo, id=compra_id)
    insumos = Insumos.objects.all().order_by('nome')

    if request.method == 'POST':
        insumo_id = int(request.POST.get('insumo'))
        compra.insumo = Insumos.objects.get(id=insumo_id)
        compra.quantidade = float(request.POST.get('quantidade', 0))
        compra.preco_total = float(request.POST.get('preco_total', 0))
        compra.data_compra = request.POST.get('data_compra') or compra.data_compra
        compra.save()
        return redirect('estoque:lista_compras_insumo')

    return render(request, 'insumos/compras_form.html', {'compra': compra, 'insumos': insumos})

def deletar_compra_insumo(request, compra_id):
    compra = get_object_or_404(CompraInsumo, id=compra_id)
    compra.delete()
    return redirect('estoque:lista_compras_insumo')
