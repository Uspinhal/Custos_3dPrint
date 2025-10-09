from flask import Blueprint, request, jsonify
from web_app.models.materia_prima import MateriaPrima, db

materia_prima_bp = Blueprint('materia_prima', __name__)

@materia_prima_bp.route('/materias-primas', methods=['GET'])
def get_materias_primas():
    """Retorna todas as matérias-primas cadastradas"""
    try:
        materias_primas = MateriaPrima.query.all()
        return jsonify([mp.to_dict() for mp in materias_primas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@materia_prima_bp.route('/materias-primas', methods=['POST'])
def create_materia_prima():
    """Cria uma nova matéria-prima"""
    data = request.get_json()
    
    required_fields = ['nome', 'quantidade', 'preco']

    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Nome, quantidade e preço são obrigatórios'}), 400
    
    try:
        materia_prima = MateriaPrima(
            nome=data['nome'],   # pyright: ignore[reportCallIssue]
            tipo=data.get('tipo'), # pyright: ignore[reportCallIssue]
            material=data.get('material'), # pyright: ignore[reportCallIssue]
            cor=data.get('cor'), # pyright: ignore[reportCallIssue]
            marca=data.get('marca'), # pyright: ignore[reportCallIssue]
            quantidade=float(data['quantidade']), # pyright: ignore[reportCallIssue]
            estoque_minimo=float(data.get('estoque_minimo', 0)), # pyright: ignore[reportCallIssue]
            preco=float(data['preco']) # pyright: ignore[reportCallIssue]
        )
        
        db.session.add(materia_prima)
        db.session.commit()
        
        return jsonify(materia_prima.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@materia_prima_bp.route('/materias-primas/<int:id>', methods=['GET'])
def get_materia_prima(id):
    """Retorna uma matéria-prima específica"""
    try:
        materia_prima = MateriaPrima.query.get_or_404(id)
        return jsonify(materia_prima.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@materia_prima_bp.route('/materias-primas/<int:id>', methods=['PUT'])
def update_materia_prima(id):
    """Atualiza uma matéria-prima existente"""
    materia_prima = MateriaPrima.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome' in data:
            materia_prima.nome = data['nome']
        if 'quantidade' in data:
            materia_prima.quantidade = float(data['quantidade'])
        if 'preco' in data:
            materia_prima.preco = float(data['preco'])
        
        db.session.commit()
        return jsonify(materia_prima.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@materia_prima_bp.route('/materias-primas/<int:id>', methods=['DELETE'])
def delete_materia_prima(id):
    """Remove uma matéria-prima"""
    try:
        materia_prima = MateriaPrima.query.get_or_404(id)
        db.session.delete(materia_prima)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    