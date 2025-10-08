# custos.py

from GUI import telas
from GUI.telas import Telas
from banco_dados import banco_dados


class CustosManager:
    def __init__(self,banco_dados):
        self.banco_dados = banco_dados

    def calcular_custo_total(self, equipamento, materia_prima_id, quantidade_utilizada, tempo_impressao):
        # Busca o tempo de impressão e o custo da matéria-prima
        materia_prima =self.banco_dados.buscar_materia_prima_por_id(materia_prima_id)
        if not materia_prima:
            raise ValueError("Matéria-prima não encontrada no banco de dados.")
        preco_materia_prima = materia_prima[0][3]
        # Calcula o custo da matéria-prima
        custo_materia_prima = self.calcular_custo_materia_prima(preco_materia_prima, quantidade_utilizada)
        # Calcula o custo com energia elétrica
        custo_energia = self.calcular_custo_energia(tempo_impressao, equipamento)
        # Soma os custos para obter o custo total
        if custo_materia_prima is None or custo_energia is None:
            return None
        custo_total = custo_materia_prima + custo_energia
        return custo_total, custo_materia_prima, custo_energia

    def calcular_custo_materia_prima(self, preco, qtd):
        try:
            custo = preco * (qtd / 1000)
            #print(f'custo mp: {custo}')
            return custo
        except Exception as e:
            print(f"Erro ao calcular o custo da matéria-prima: {e}")
            return None 
    
    def calcular_custo_energia(self, tempo_impressao, equipamento):
        try: 
            custo_kwh = self.banco_dados.buscar_insumo_por_nome('Energia')[4]
            consumo_energia = (equipamento[2] / 1000) * (tempo_impressao / 60)
            custo_energia = consumo_energia * custo_kwh
            #print(f"custo energia: {custo_energia}")
            return custo_energia
        except Exception as e:
            print(f"Erro ao calcular o custo com energia elétrica: {e}")
            return None
           