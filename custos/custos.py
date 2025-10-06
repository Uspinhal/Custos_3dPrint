# custos.py

from GUI import telas
from GUI.telas import Telas
from banco_dados import banco_dados


class CustosManager:
    def __init__(self,banco_dados):
        self.banco_dados = banco_dados
        self.telas = Telas("dados.db")

    def calcular_custo_total(self):
        # Calcula os custos totais
        # Escolha do equipamento
        equipamento = self.telas.escolher_equipamentos(self.banco_dados)
        # Escolha da mantéria-prima
        id_mp = self.telas.mostrar_opcoes_materia_prima()
        preco = self.banco_dados.obter_preco_materia_prima(id_mp)[0][0]
        # Quantidade de matéria-prima utilizada
        qtd = self.telas.obter_quantidade_utilizada()
        # Entrar com tempo de impressão
        tempo_impressao = self.telas.obter_tempo_impressao()
        
        custo_materia_prima = self.calcular_custo_materia_prima(preco, qtd)
        custo_energia = self.calcular_custo_energia(tempo_impressao, equipamento)
               
        custo_total = custo_materia_prima + custo_energia # type: ignore
        
        self.telas.mostrar_custos(custo_total)

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
           