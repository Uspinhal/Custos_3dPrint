# tela_inicial.py
from banco_dados.banco_dados import BancoDados

class Telas():
    def __init__(self, db_file):
        """
        Inicializa a classe Telas.

        Parâmetros:
            db_file (str): O caminho para o arquivo do banco de dados.
        """
        self.db_file = BancoDados(db_file)

    @staticmethod
    def tela_inicial():
        """
        Exibe a tela inicial do aplicativo.
        """
        print("Bem-vindo ao aplicativo de controle de custos e precificação de produção de impressões 3D.")
        print("Escolha uma opção:")
        print("1. Adicionar matéria-prima")
        print("2. Adicionar equipamento")
        print("3. Adicionar insumo")
        print("4. Calcular custos")
        print("5. Mostrar custos")
        print("6. Sair")
    
    @staticmethod
    def obter_quantidade_utilizada():
        """
        Solicita ao usuário a quantidade de matéria-prima utilizada.

        Retorna:
            float: A quantidade de matéria-prima utilizada.
        """
        while True:
            try:
                quantidade_utilizada = float(input("Digite a quantidade de matéria-prima utilizada (em gramas): "))
                return quantidade_utilizada
            except ValueError:
                print("Erro: Digite um número válido para a quantidade de matéria-prima utilizada.")

    @staticmethod
    def mostrar_opcoes_equipamentos(opcoes_equipamentos):
        """
        Exibe as opções de equipamentos disponíveis.

        Parâmetros:
            opcoes_equipamentos (list): Lista de opções de equipamentos.
        """
        try:
            if not opcoes_equipamentos:
                raise ValueError("Não há opções de equipamentos disponíveis.")
            
            print("Equipamentos disponíveis:")
            for idx, equipamento in enumerate(opcoes_equipamentos, start=1):
                print(f"{idx}. {equipamento[1]} - Potência: {equipamento[2]} W")

        except ValueError as ve:
            print(f"Erro: {ve}")
            return None

    @staticmethod
    def escolher_equipamentos(banco_dados):
        """
        Permite ao usuário escolher um equipamento.

        Parâmetros:
            banco_dados (BancoDados): Instância do objeto BancoDados.

        Retorna:
            tuple: As informações do equipamento escolhido.
        """
        equipamentos = BancoDados.obter_equipamentos(banco_dados)

        Telas.mostrar_opcoes_equipamentos(equipamentos)
        try:
            opcao = int(input("Escolha o número correspondente ao equipamento: "))
            if opcao < 1 or opcao > len(equipamentos):
                raise ValueError("Opção inválida.")
            return equipamentos[opcao - 1]
        
        except ValueError as ve:
            print(f"Erro: {ve}")
            return None       

    @staticmethod
    def obter_tempo_impressao():
        """
        Solicita ao usuário o tempo de impressão.

        Retorna:
            float: O tempo de impressão em minutos.
        """
    # Entrada para o tempo de impressão
        while True:
            try:
                tempo_impressao = float(input("Digite o tempo de impressão (em minutos): "))
                return tempo_impressao
            except ValueError:
                print("Erro: Digite um número válido para o tempo de impressao.")

    def mostrar_opcoes_materia_prima(self):
        """
        Exibe as opções de matéria-prima disponíveis.
        """
        try:
            opcoes_materia_prima = self.db_file.obter_opcoes_materias_primas()
            if not opcoes_materia_prima:
                raise Exception("Não há opções de matéria-prima disponíveis.")        
            print("Matérias-primas disponíveis:")
            for materia_prima in opcoes_materia_prima:
                print(f"{materia_prima[0]}. {materia_prima[1]} - R${materia_prima[3]}")

            while True:
                try:
                    opcao = int(input("Digite o número correspondente à matéria-prima escolhida: "))
                    if opcao < 1 or opcao > len(opcoes_materia_prima):
                        raise ValueError("Opção inválida. Digite um número dentro do intervalo válido.")
                    return opcao
                except ValueError as ve:
                    print(f"Erro: {ve}")


        except Exception as e:
            print(f"Erro ao obter opções de matéria-prima: {e}")
    
    def mostrar_custos(self, custo):
        """
        Exibe o custo total calculado.

        Parâmetros:
            custo (float): O custo total calculado.
        """
        try:
            print(f"O custo total é: R${custo:.2f}")
        except TypeError:
            print("Erro ao exibir o custo.")
        
