# banco_dados.py
import re
import sqlite3

class BancoDados:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def conectar(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def criar_tabela(self):
        """Cria as tabelas do Banco de Dados"""
        if not self.conn:
            print("Conexão com o banco de dados não estabelecida.")
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS materia_prima (
                                id INTEGER PRIMARY KEY,
                                nome TEXT NOT NULL UNIQUE,
                                quantidade REAL,
                                preco REAL
                             )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS insumos (
                                id INTEGER PRIMARY KEY,
                                nome TEXT NOT NULL UNIQUE,
                                quantidade REAL,
                                unidade TEXT,
                                preco REAL
                             )''')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            return False
           
    # Métodos genéricos para manipulação do banco de dados
    def executar_query(self, sql, params=()):
        """Executa uma query e retorna todos os resultados."""
        if not self.conn:
            print("Conexão com o banco de dados não estabelecida.")
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall() 
            return results
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            return []

    def executar_modificacao(self, sql, params=()):
        """Executa uma query de modificação (INSERT, UPDATE, DELETE) no banco de dados."""
        if not self.conn:
            print("Conexão com o banco de dados não estabelecida.")
            return None
        
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(sql, params)
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao executar modificação: {e}")
            self.conn.rollback()
            return None


    # Métodos para Matéria-Prima
    def adicionar_materia_prima(self, nome, quantidade, preco):
        query = "INSERT INTO materiaPrima (nome, quantidade, preco) VALUES (?, ?, ?)"
        return self.executar_modificacao(query, (nome, quantidade, preco))

    def obter_materia_prima(self):
        query = "SELECT * FROM materia_prima"
        return self.executar_query(query)
    
    def buscar_materia_prima_por_id(self, mp_id):
        """ 
        Busca uma matéria-prima pelo ID no banco de dados.

        Retorna uma tupla com os dados da matéria-prima ou None se não for encontrado.
        """
        query = "SELECT * FROM materia_prima WHERE id = ?"
        resultados = self.executar_query(query, (mp_id,))
        return resultados[0] if resultados else None

    # Métodos para Equipamento
    def adicionar_equipamento(self, nome, potencia, preco, valor_inicial, vida_util):
        query = "INSERT INTO equipamento (nome, potencia, preco, valor_inicial, vida_util) VALUES (?, ?, ?, ?, ?)"
        return self.executar_modificacao(query, (nome, potencia, preco, valor_inicial, vida_util))
    
    def obter_equipamentos(self):
        query = "SELECT * FROM equipamento"
        return self.executar_query(query)

    # Métodos para Insumos
    def adicionar_insumo(self, nome, quantidade, unidade, preco):
        query = "INSERT INTO insumos (nome, quantidade, unidade, preco) VALUES (?, ?, ?, ?)"
        return self.executar_modificacao(query, (nome, quantidade, unidade, preco))
    
    def obter_insumos(self):
        query = "SELECT * FROM insumos"
        return self.executar_query(query)
        
    def buscar_insumo_por_nome(self, nome):
        """ 
        Busca um insumo pelo nome no banco de dados.

        Retorna uma tupla com os dados do insumo ou None se não for encontrado.
        """
        query = "SELECT * FROM insumos WHERE nome = ?"
        resultados = self.executar_query(query, (nome,))
        return resultados[0] if resultados else None
