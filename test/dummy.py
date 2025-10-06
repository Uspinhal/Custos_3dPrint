from banco_dados.banco_dados import BancoDados

def adicionar_campos_equipamentos(db_file):
    # Inicializa o objeto BancoDados
    banco_dados = BancoDados(db_file)

    # Define a instrução SQL para adicionar a coluna 'valor_inicial' à tabela 'equipamentos'
    sql_valor_inicial = """
    ALTER TABLE equipamento
    ADD COLUMN valor_inicial REAL
    """

    # Define a instrução SQL para adicionar a coluna 'vida_util' à tabela 'equipamentos'
    sql_vida_util = """
    ALTER TABLE equipamento
    ADD COLUMN vida_util INTEGER
    """

    try:
        # Executa as instruções SQL
        banco_dados.execute(sql_valor_inicial)
        banco_dados.execute(sql_vida_util)
        print("Campos adicionados com sucesso à tabela equipamentos!")
    except Exception as e:
        print(f"Erro ao adicionar os campos à tabela equipamentos: {e}")

# Substitua "dados.db" pelo nome do seu arquivo de banco de dados SQLite
db_file = "dados.db"

# Chama a função para adicionar os campos à tabela equipamentos
adicionar_campos_equipamentos(db_file)
