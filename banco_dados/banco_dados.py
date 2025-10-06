# banco_dados.py
import sqlite3

class BancoDados:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        """
        Cria as tabelas do Banco de Dados
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        # Tabela para materia prima
        c.execute('''CREATE TABLE IF NOT EXISTS materiaPrima (
                        id INTEGER PRIMARY KEY,
                        nome TEXT,
                        quantidade REAL,
                        preco REAL
                     )''')
        # Tabela para equipamento
        c.execute('''CREATE TABLE IF NOT EXISTS equipamento (
                        id INTEGER PRIMARY KEY,
                        nome TEXT,
                        potencia REAL,
                        preco REAL
                     )''')
        # Tabela para insumos
        c.execute('''CREATE TABLE IF NOT EXISTS insumos (
                        id INTEGER PRIMARY KEY,
                        nome TEXT,
                        quantidade REAL,
                        unidade TEXT,
                        preco REAL
                     )''')
        conn.commit()
        conn.close()
    
    # Métodos genéricos para manipulação do banco de dados
    def query(self, sql, params=None):
        """
        Realiza consultas no banco de dados e retorna todos os resultados
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        rows = c.fetchall()
        conn.close()
        return rows

    def execute(self, sql, params=None):
        """
        Executa manipulações no Banco de Dados
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        conn.commit()
        conn.close()
  
    def mostrar_tabelas(self, tabela):
        """
        Mostra a tabela selecionada
        """
        sql = f"SELECT * FROM {tabela}"

        dados = self.query(sql)

        if dados:
            for linha in dados:
                print(linha)
        else:
            print(f"A tabela '{tabela}' está vazia.")  


    # Métodos para operações específicas em cada tabela

    # Matéria Prima
    def adicionar_materia_prima(self, nome, quantidade, preco):
        sql = "INSERT INTO materiaPrima (nome, quantidade, preco) VALUES (?, ?, ?)"
        params = (nome, quantidade, preco)
        return self.execute(sql, params)
        #conn = sqlite3.connect(self.db_file)
        #c = conn.cursor()
        #c.execute("INSERT INTO materiaPrima (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        #conn.commit()
        #conn.close()

    def atualizar_materia_prima(self, id, nome, quantidade, preco):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("UPDATE materiaPrima SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id))
        conn.commit()
        conn.close()

    def excluir_materia_prima(self, id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM materiaPrima WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def buscar_materia_prima_por_nome(self, nome):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM materiaPrima WHERE nome=?", (nome,))
        row = c.fetchone()
        conn.close()
        return row

    def obter_opcoes_materias_primas(self):
        sql = "SELECT * FROM materiaPrima"
        return self.query(sql)
    
    def obter_preco_materia_prima(self, id_materia_prima):
        sql = "SELECT preco FROM materiaPrima WHERE id=?"
        params = (id_materia_prima,)
        result = self.query(sql, params)
        return result if result else None

    # Equipamentos
    def adicionar_equipamento(self, nome, potencia, preco, valor_inicial, vida_util):
        sql = "INSERT INTO equipamento (nome, potencia, preco, valor_inicial, vida_util) VALUES (?, ?, ?, ?, ?)"
        params = (nome, potencia, preco, valor_inicial, vida_util)
        self.execute(sql, params)

    def atualizar_equipamento(self, id, nome, potencia, preco):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("UPDATE equipamento SET nome=?, potencia=?, preco=? WHERE id=?", (nome, potencia, preco, id))
        conn.commit()
        conn.close()

    def excluir_equipamento(self, id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM equipamento WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def buscar_equipamento_por_nome(self, nome):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM equipamento WHERE nome=?", (nome,))
        row = c.fetchone()
        conn.close()
        return row

    def obter_equipamentos(self):
        sql = "SELECT * FROM equipamento"
        equipamentos = self.query(sql)
        return equipamentos

    # Insumos
    def adicionar_insumo(self, nome, quantidade, unidade, preco):
        sql = "INSERT INTO insumos (nome, quantidade, unidade, preco) VALUES (?, ?, ?, ?)"
        params = (nome, quantidade, unidade, preco)
        self.execute(sql, params)
        #conn = sqlite3.connect(self.db_file)
        #c = conn.cursor()
        #c.execute("INSERT INTO insumos (nome, quantidade, unidade, preco) VALUES (?, ?, ?, ?)", (nome, quantidade, unidade, preco))
        #conn.commit()
        #conn.close()

    def atualizar_insumo(self, id, nome, quantidade, unidade, preco):
        sql = "UPDATE insumos SET nome=?, quantidade=?, unidade=?, preco=? WHERE id=?"
        params = (nome, quantidade, unidade, preco, id)
        self.execute(sql, params)
        
        #conn = sqlite3.connect(self.db_file)
        #c = conn.cursor()
        #c.execute("UPDATE insumos SET nome=?, quantidade=?, unidade=?, preco=? WHERE id=?", (nome, quantidade, unidade, preco, id))
        #conn.commit()
        #conn.close()

    def excluir_insumo(self, id):
        sql = "DELETE FROM insumos WHERE id=?"
        params = (id,)
        self.execute(sql, params)
        
        #conn = sqlite3.connect(self.db_file)
        #c = conn.cursor()
        #c.execute("DELETE FROM insumos WHERE id=?", (id,))
        #conn.commit()
        #conn.close()

    def buscar_insumo_por_nome(self, nome):
        """ 
        Busca um insumo pelo nome no banco de dados.

        Retorna uma tupla com os dados do insumo ou None se não for encontrado.
        """
        sql = "SELECT * FROM insumos WHERE nome=?"
        params = (nome,)
        try:
            with sqlite3.connect(self.db_file) as conn:
                c = conn.cursor()
                c.execute(sql, params)
                row = c.fetchone()
                return row
        except sqlite3.Error as e:
            print(f"Erro ao buscar insumo por nome: {e}")
            return None       
        #try:
        #    sql = "SELECT * FROM insumos WHERE nome=?"
        #    params = (nome,)
        #    self.query(sql, params)
        
        #except Exception as e:
        #    print(f'Erro ao buscar. {e}')
