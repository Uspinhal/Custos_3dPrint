# main.py
from banco_dados.banco_dados import BancoDados
from GUI.telas import Telas
from custos.custos import CustosManager

banco_dados = BancoDados("dados.db")
telas = Telas("dados.db")
custos = CustosManager(banco_dados)

def mostar_tabelas():
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    tabelas = banco_dados.query(sql)

    for tabela in tabelas:
        print(f"\nConteúdo da tabela '{tabela[0]}':")
        sql = f"SELECT * FROM {tabela[0]}"
        #print(sql)     
        dados = banco_dados.query(sql)
        
        if dados:
            for linha in dados:
                print(linha)
        else:
            print(f"A tabela {tabela[0]} está vazia")   

def calculo_custo(banco_dados):
    # Escolhe o equipamento a ser utilizado
    maquina = telas.escolher_equipamentos(banco_dados)
    print(maquina)
    # Escolhe qual matéria-prima a ser utilizada
    id_mp = telas.mostrar_opcoes_materia_prima()
    preco_materia_prima = banco_dados.obter_preco_materia_prima(id_mp)
    # Entra com a quantidade de matéria-prima utilizada
    quantidade_utlilizada = telas.obter_quantidade_utilizada()
    # Chama o cálculo de custos e mostra na tela.
    telas.mostrar_custos(custos.calcular_custo_total())


custos.calcular_custo_total()
banco_dados.mostrar_tabelas('insumos')

energia = banco_dados.buscar_insumo_por_nome('Energia')
print(type(energia))
print(f"O valor do kWh é R${energia[4]:.2f}") # type: ignore