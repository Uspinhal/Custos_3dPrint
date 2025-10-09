from .materia_prima import db

class Equipamento(db.Model):
    """Modelo para equipamentos de impressão 3D"""
    __tablename__ = 'equipamento'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    potencia = db.Column(db.Float, nullable=False)  # em watts
    preco = db.Column(db.Float, nullable=False)  # preço atual
    valor_inicial = db.Column(db.Float, nullable=False)  # valor de compra
    vida_util = db.Column(db.Float, nullable=False)  # em horas
    
    def to_dict(self):
        """Converte o objeto para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'potencia': self.potencia,
            'preco': self.preco,
            'valor_inicial': self.valor_inicial,
            'vida_util': self.vida_util
        }
    
    def __repr__(self):
        return f'<Equipamento {self.nome}>'