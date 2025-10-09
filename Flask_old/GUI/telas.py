# GUI/telas.py

class Telas:
    @staticmethod
    def tela_inicial():
        """Exibe a tela inicial do aplicativo."""
        print("Bem-vindo ao aplicativo de controle de custos e precificação de produção de impressões 3D.")
        print("Escolha uma opção:")
        print("1. Adicionar matéria-prima")
        print("2. Adicionar equipamento")
        print("3. Adicionar insumo")
        print("4. Calcular custos")
        print("5. Sair")

    @staticmethod
    def obter_dados_materia_prima():
        """Solicita ao usuário os dados para uma nova matéria-prima."""
        try:
            nome = input("Nome: ")
            quantidade = float(input("Quantidade: "))
            preco = float(input("Preço por unidade: R$"))
            return nome, quantidade, preco
        except ValueError:
            print("Erro: Valor inválido. Certifique-se de inserir números para quantidade e preço.")
            return None, None, None

    @staticmethod
    def obter_dados_equipamento():
        """Solicita ao usuário os dados para um novo equipamento."""
        try:
            nome = input("Nome: ")
            potencia = float(input("Potência (W): "))
            preco = float(input("Preço: R$"))
            valor_inicial = float(input("Valor inicial: R$"))
            vida_util = float(input("Vida útil (horas): "))
            return nome, potencia, preco, valor_inicial, vida_util
        except ValueError:
            print("Erro: Valor inválido. Certifique-se de inserir números para os campos.")
            return None, None, None, None, None

    @staticmethod
    def obter_dados_insumo():
        """Solicita ao usuário os dados para um novo insumo."""
        try:
            nome = input("Nome: ")
            quantidade = float(input("Quantidade: "))
            unidade = input("Unidade: ")
            preco = float(input("Preço por unidade: R$"))
            return nome, quantidade, unidade, preco
        except ValueError:
            print("Erro: Valor inválido. Certifique-se de inserir números para quantidade e preço.")
            return None, None, None, None

    @staticmethod
    def escolher_item(itens, tipo_item):
        """Exibe uma lista de itens e solicita ao usuário que escolha um."""
        if not itens:
            print(f"Não há {tipo_item}s cadastrados.")
            return None

        print(f"{tipo_item.capitalize()}s disponíveis:")
        for i, item in enumerate(itens):
            print(f"{i + 1}. {item[1]}")

        while True:
            try:
                escolha = int(input(f"Escolha o número do {tipo_item}: "))
                if 1 <= escolha <= len(itens):
                    return itens[escolha - 1]
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Erro: Digite um número.")

    @staticmethod
    def obter_quantidade_utilizada():
        """Solicita ao usuário a quantidade de matéria-prima utilizada."""
        while True:
            try:
                return float(input("Digite a quantidade de matéria-prima utilizada (em gramas): "))
            except ValueError:
                print("Erro: Digite um número válido.")

    @staticmethod
    def obter_tempo_impressao():
        """Solicita ao usuário o tempo de impressão."""
        while True:
            try:
                return float(input("Digite o tempo de impressão (em minutos): "))
            except ValueError:
                print("Erro: Digite um número válido.")

    @staticmethod
    def mostrar_custos(custo_total, custo_materia_prima, custo_energia):
        """Exibe os custos calculados."""
        print("\n--- Resultado do Cálculo de Custos ---")
        print(f"Custo com matéria-prima: R${custo_materia_prima:.2f}")
        print(f"Custo com energia elétrica: R${custo_energia:.2f}")
        print(f"Custo total da impressão: R${custo_total:.2f}")
