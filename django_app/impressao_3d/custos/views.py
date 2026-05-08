from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import CalculadoraCustosResina, CalculadoraCustosFilamento

from django.shortcuts import render
from django.views import View
from .forms import CalculoCustosForm, TempoImpressaoField
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
            num_mesas = int(request.POST.get("num_mesas", 1))

            # Campos obrigatórios apenas quando mesa única
            if num_mesas == 1:
                if not form.cleaned_data.get("quantidade"):
                    form.add_error("quantidade", "Campo obrigatório.")
                    return render(request, "custos/calcular.html", {"form": form})
                if not form.cleaned_data.get("tempo_horas"):
                    form.add_error("tempo_horas", "Campo obrigatório.")
                    return render(request, "custos/calcular.html", {"form": form})

            tipo = form.cleaned_data["tipo"]
            equipamento = form.cleaned_data["equipamento"]
            materia_prima = form.cleaned_data["materia_prima"]
            quantidade = form.cleaned_data["quantidade"]
            tempo_horas = form.cleaned_data["tempo_horas"]
            taxa_perda = form.cleaned_data["taxa_perda"]

            if tipo == "resina":
                unidade_resina = form.cleaned_data.get("unidade_resina", "g")
                num_mesas = int(request.POST.get("num_mesas", 1))

                if num_mesas == 1:
                    quantidade_g = quantidade * 1.2 if unidade_resina == "ml" else quantidade
                    mesas = [{'quantidade_g': float(quantidade_g), 'tempo_horas': float(tempo_horas)}]
                else:
                    mesas = []
                    for i in range(1, num_mesas + 1):
                        qtd = float(request.POST.get(f'mesa_{i}_quantidade', 0) or 0)
                        tempo = TempoImpressaoField().to_python(request.POST.get(f'mesa_{i}_tempo', '0') or '0')
                        quantidade_g = qtd * 1.2 if unidade_resina == "ml" else qtd
                        mesas.append({'quantidade_g': quantidade_g, 
                                      'tempo_horas': tempo})


                calculadora = CalculadoraCustosResina(
                    equipamento_id=equipamento.id,
                    mesas=mesas,
                    taxa_perda=taxa_perda,
                    materia_prima_id=materia_prima.id
                )
            else:
                num_mesas = int(request.POST.get("num_mesas", 1))
                
                if num_mesas == 1:
                    mesas = [{'quantidade_g': float(quantidade), 'tempo_horas': float(tempo_horas)}]
                else:
                    mesas = []
                    for i in range(1, num_mesas + 1):
                        mesas.append({
                            'quantidade_g': float(request.POST.get(f'mesa_{i}_quantidade', 0) or 0),
                            'tempo_horas': TempoImpressaoField().to_python(request.POST.get(f'mesa_{i}_tempo', '0') or '0'),
                        })
                
                calculadora = CalculadoraCustosFilamento(
                    equipamento_id=equipamento.id,
                    mesas=mesas,
                    taxa_perda=taxa_perda,
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
            # Suporta formato antigo (single) e novo (mesas)
            mesas_raw = dados.get("mesas")
            if mesas_raw:
                mesas = [
                    {
                        'quantidade_g': float(m.get('quantidade_resina_g', 0)),
                        'tempo_horas': float(m.get('tempo_horas', 0)),
                    }
                    for m in mesas_raw
                ]
            else:
                # Compatibilidade retroativa
                mesas = [{'quantidade_g': float(dados.get('quantidade_resina_g', 0)),
                          'tempo_horas': float(dados.get('tempo_horas', 0))}]

            calculadora = CalculadoraCustosResina(
                equipamento_id=dados.get("equipamento_id"),
                mesas=mesas,
                taxa_perda=float(dados.get("taxa_perda", 5)),
                materia_prima_id=dados.get("materia_prima_id"),
            )

        elif tipo == "filamento":
            mesas_raw = dados.get("mesas")
            if mesas_raw:
                mesas = [
                    {
                        'quantidade_g': float(m.get('quantidade_filamento_g', 0)),
                        'tempo_horas': float(m.get('tempo_horas', 0)),
                    }
                    for m in mesas_raw
                ]
            else:
                mesas = [{'quantidade_g': float(dados.get('quantidade_filamento_g', 0)),
                          'tempo_horas': float(dados.get('tempo_horas', 0))}]

            calculadora = CalculadoraCustosFilamento(
                equipamento_id=dados.get("equipamento_id"),
                mesas=mesas,
                materia_prima_id=dados.get("materia_prima_id"),
            )

        else:
            return Response({"erro": "Tipo de impressão inválido"}, status=status.HTTP_400_BAD_REQUEST)

        custo_total = calculadora.calcular_custo_total()
        return Response({"custo_total": custo_total})