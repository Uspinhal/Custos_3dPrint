from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MateriaPrima(db.Model):
    """Modelo para matérias-primas utilizadas na impressão 3D"""
    __tablename__ = 'materia_prima'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Nome descritivo
    tipo = db.Column(db.String(20), nullable=True)   # Filamento/Resina
    material = db.Column(db.String(30), nullable=True)  # PLA, ABS-Like, etc
    cor = db.Column(db.String(30), nullable=True)
    marca = db.Column(db.String(50), nullable=True)
    quantidade = db.Column(db.Float, nullable=False)  # Estoque atual
    estoque_minimo = db.Column(db.Float, nullable=False)  # Para alertas
    preco = db.Column(db.Float, nullable=False)  # Preço por unidade (kg, litro, etc)

    def to_dict(self):
        """Converte o objeto para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'material': self.material,
            'cor': self.cor,
            'marca': self.marca,
            'quantidade': self.quantidade,
            'estoque_minimo': self.estoque_minimo,
            'preco': self.preco

        }
    
    def __repr__(self):
        return f'<MateriaPrima {self.nome}>'
    