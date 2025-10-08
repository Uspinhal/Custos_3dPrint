# main.py
import os
from banco_dados.banco_dados import BancoDados
from custos.custos import CustosManager
from GUI.telas import Telas

DB_FILE = "dados.db"

def limpar_tela():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def adicionar_materia_prima(banco_dados):
    """Adiciona uma nova matéria-prima ao banco de dados."""
    nome, quantidade, preco = Telas.obter_dados_materia_prima()
    if nome and quantidade is not None and preco is not None:
        banco_dados.adicionar_materia_prima(nome, quantidade, preco)
        print("Matéria-prima adicionada com sucesso!")

def adicionar_equipamento(banco_dados):
    """Adiciona um novo equipamento ao banco de dados."""
    nome, potencia, preco, valor_inicial, vida_util = Telas.obter_dados_equipamento()
    if nome and potencia and preco and valor_inicial and vida_util:
        banco_dados.adicionar_equipamento(nome, potencia, preco, valor_inicial, vida_util)
        print("Equipamento adicionado com sucesso!")

def adicionar_insumo(banco_dados):
    """Adiciona um novo insumo ao banco de dados."""
    nome, quantidade, unidade, preco = Telas.obter_dados_insumo()
    if nome and quantidade and unidade and preco:
        banco_dados.adicionar_insumo(nome, quantidade, unidade, preco)
        print("Insumo adicionado com sucesso!")

def calcular_custos(banco_dados, custos_manager):
    """Calcula os custos de uma impressão."""
    # Selecionar equipamento
    equipamentos = banco_dados.obter_equipamentos()
    equipamento_escolhido = Telas.escolher_item(equipamentos, "equipamento")
    if not equipamento_escolhido:
        return

    # Selecionar matéria-prima
    materias_primas = banco_dados.obter_materias_primas()
    materia_prima_escolhida = Telas.escolher_item(materias_primas, "matéria-prima")
    if not materia_prima_escolhida:
        return

    # Obter dados da impressão
    quantidade_utilizada = Telas.obter_quantidade_utilizada()
    tempo_impressao = Telas.obter_tempo_impressao()

    # Calcular e exibir os custos
    try:
        custo_total, custo_materia_prima, custo_energia = custos_manager.calcular_custo_total(
            equipamento_escolhido,
            materia_prima_escolhida[0], # ID da matéria-prima
            quantidade_utilizada,
            tempo_impressao
        )
        Telas.mostrar_custos(custo_total, custo_materia_prima, custo_energia)
    except (ValueError, TypeError) as e:
        print(f"Erro ao calcular custos: {e}")

def main():
    """Função principal que inicia a aplicação."""
    banco_dados = BancoDados(DB_FILE)
    banco_dados.conectar()
    banco_dados.criar_tabela()

    custos_manager = CustosManager(banco_dados)

    while True:
        limpar_tela()
        Telas.tela_inicial()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            limpar_tela()
            adicionar_materia_prima(banco_dados)
            input("\nPressione Enter para continuar...")
        elif opcao == "2":
            limpar_tela()
            adicionar_equipamento(banco_dados)
            input("\nPressione Enter para continuar...")
        elif opcao == "3":
            limpar_tela()
            adicionar_insumo(banco_dados)
            input("\nPressione Enter para continuar...")
        elif opcao == "4":
            limpar_tela()
            calcular_custos(banco_dados, custos_manager)
            input("\nPressione Enter para continuar...")
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")

    banco_dados.desconectar()

if __name__ == "__main__":
    main()
