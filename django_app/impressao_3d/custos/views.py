from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import CalculadoraCustosResina, CalculadoraCustosFilamento

from django.shortcuts import render
from django.views import View
from .forms import CalculoCustosForm
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima, Insumos


# 🔹 View HTML — para o navegador
def calcular_custo_view(request):
    result = None
    breakdown = {}
    tipo = None

    # Tipo vindo da URL (?tipo=resina) para filtrar os dropdowns antes do POST
    tipo_get = request.GET.get("tipo")

    if request.method == "POST":
        form = CalculoCustosForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data["tipo"]
            equipamento = form.cleaned_data["equipamento"]
            materia_prima = form.cleaned_data["materia_prima"]
            quantidade = form.cleaned_data["quantidade"]
            tempo_horas = form.cleaned_data["tempo_horas"]
            taxa_perda = form.cleaned_data["taxa_perda"]

            if tipo == "resina":
                calculadora = CalculadoraCustosResina(
                    equipamento_id=equipamento.id,
                    quantidade_resina_g=quantidade,
                    tempo_horas=tempo_horas,
                    taxa_perda=taxa_perda,
                    materia_prima_id=materia_prima.id
                )
            else:
                calculadora = CalculadoraCustosFilamento(
                    equipamento_id=equipamento.id,
                    quantidade_filamento_g=quantidade,
                    tempo_horas=tempo_horas,
                    materia_prima_id=materia_prima.id
                )

            result = calculadora.calcular_custo_total()
            breakdown = calculadora.detalhar_custos()

    else:
        # Passa tipo do GET para o form para filtrar equipamentos e matérias-primas
        form = CalculoCustosForm(initial={"tipo": tipo_get}, tipo=tipo_get)

    return render(request, "custos/calcular.html", {
        "form": form, 
        "result": result, 
        "breakdown": breakdown,
        "tipo": tipo,
        })



# 🔹 View API — para integração externa
class CalcularCustoAPI(APIView):
    def post(self, request):
        tipo = request.data.get("tipo")
        dados = request.data

        if tipo == "resina":
            calculadora = CalculadoraCustosResina(
                equipamento_id=dados.get("equipamento_id"),
                quantidade_resina_g=float(dados.get("quantidade_resina_g", 0)),
                tempo_horas=float(dados.get("tempo_horas", 0)),
                taxa_perda=float(dados.get("taxa_perda", 5)),
            )
        elif tipo == "filamento":
            calculadora = CalculadoraCustosFilamento(
                equipamento_id=dados.get("equipamento_id"),
                quantidade_filamento_g=float(dados.get("quantidade_filamento_g", 0)),
                tempo_horas=float(dados.get("tempo_horas", 0)),
            )
        else:
            return Response({"erro": "Tipo de impressão inválido"}, status=status.HTTP_400_BAD_REQUEST)

        custo_total = calculadora.calcular_custo_total()
        return Response({"custo_total": custo_total})