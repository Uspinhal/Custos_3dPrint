# main.py
import os
from banco_dados.banco_dados import BancoDados
from custos.custos import CustosManager
from GUI.telas import Telas

DB_FILE = "dados.db"

def limpar_tela():
    """
    Limpa a tela do console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def adicionar_materia_prima(banco_dados):
    """
    Adiciona uma nova matéria-prima ao banco de dados.

    Args:
        banco_dados (BancoDados): Objeto para interação com o banco de dados.

    """
    try:
        nome = input("Nome: ")
        quantidade = float(input("Quantidade: "))
        preco = float(input("Preço por unidade: R$"))
        banco_dados.adicionar_materia_prima(nome, quantidade, preco)
        print("Matéria-prima adicionada com sucesso!")
    except ValueError:
        print("Erro: Valor inválido. Certifique-se de inserir números para quantidade e preço.")
    except Exception as e:
        print(f"Erro ao adicionar matéria-prima: {e}")

def adicionar_equipamento(banco_dados):
    """
    Adiciona um novo equipamento ao banco de dados.

    Args:
        banco_dados (BancoDados): Objeto para interação com o banco de dados.
    """
    try:
        nome = input("Nome: ")
        potencia = float(input("Potência (W): "))
        preco = float(input("Preço: R$"))
        banco_dados.adicionar_equipamento(nome, potencia, preco)
        print("Equipamento adicionado com sucesso!")
    except ValueError:
        print("Erro: Valor inválido. Certifique-se de inserir números para potência e preço.")
    except Exception as e:
        print(f"Erro ao adicionar equipamento: {e}")

def adicionar_insumo(banco_dados):
    """
    Adiciona um novo insumo ao banco de dados.

    Args:
        banco_dados (BancoDados): Objeto para interação com o banco de dados.
    """
    try:
        nome = input("Nome: ")
        quantidade = float(input("Quantidade: "))
        unidade = input("Unidade: ")
        preco = float(input("Preço por unidade: R$"))
        banco_dados.adicionar_insumo(nome, quantidade, unidade, preco)
        print("Insumo adicionado com sucesso!")
    except ValueError:
        print("Erro: Valor inválido. Certifique-se de inserir números para quantidade e preço.")
    except Exception as e:
        print(f"Erro ao adicionar insumo: {e}")



def main():
    """
    Função principal que inicia a aplicação.
    """
    banco_dados = BancoDados(DB_FILE)
    custos_manager = CustosManager(banco_dados)
    telas = Telas(DB_FILE)
    while True:
        limpar_tela()
        telas.tela_inicial()
        opcao = input("Escolha uma opção: ")
        try:
            if opcao == "1":
                limpar_tela()
                adicionar_materia_prima(banco_dados)
                input("Pressione Enter para continuar...")
            elif opcao == "2":
                limpar_tela()
                adicionar_equipamento(banco_dados)
                input("Pressione Enter para continuar...")
            elif opcao == "3":
                limpar_tela()
                adicionar_insumo(banco_dados)
                input("Pressione Enter para continuar...")
            elif opcao == "4":
                limpar_tela()
                custos_manager.calcular_custo_total()
                input("Pressione Enter para continuar...")
            elif opcao == "5":
                limpar_tela()
                print('TBD')
                input("Pressione Enter para continuar...")
            elif opcao == "6":
                break
            else:
                print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")
        
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()
