from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

def materias_primas_view(request):
    return render(request, 'materias_primas/lista.html')

def insumos_view(request):
    return render(request, 'insumos/lista.html')

def equipamentos_view(request):
    return render(request, 'equipamentos/lista.html')