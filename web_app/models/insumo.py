from .materia_prima import db

class Insumo(db.Model):
    """Modelo para insumos diversos (energia, etc.)"""
    __tablename__ = 'insumos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20), nullable=False)  # kWh, unidade, etc.
    preco = db.Column(db.Float, nullable=False)  # preço por unidade
    
    def to_dict(self):
        """Converte o objeto para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'unidade': self.unidade,
            'preco': self.preco
        }
    
    def __repr__(self):
        return f'<Insumo {self.nome}>'