from flask import Blueprint, request, jsonify
from web_app.models.insumo import Insumo, db

insumo_bp = Blueprint('insumo', __name__)

@insumo_bp.route('/insumos', methods=['GET'])
def get_insumos():
    """Retorna todos os insumos cadastrados"""
    try:
        insumos = Insumo.query.all()
        return jsonify([insumo.to_dict() for insumo in insumos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@insumo_bp.route('/insumos', methods=['POST'])
def create_insumo():
    """Cria um novo insumo"""
    data = request.get_json()
    
    required_fields = ['nome', 'quantidade', 'unidade', 'preco']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        insumo = Insumo(
            nome=data['nome'],
            quantidade=float(data['quantidade']),
            unidade=data['unidade'],
            preco=float(data['preco'])
        )
        
        db.session.add(insumo)
        db.session.commit()
        
        return jsonify(insumo.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@insumo_bp.route('/insumos/<int:id>', methods=['GET'])
def get_insumo(id):
    """Retorna um insumo específico"""
    try:
        insumo = Insumo.query.get_or_404(id)
        return jsonify(insumo.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@insumo_bp.route('/insumos/<int:id>', methods=['PUT'])
def update_insumo(id):
    """Atualiza um insumo existente"""
    insumo = Insumo.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome' in data:
            insumo.nome = data['nome']
        if 'quantidade' in data:
            insumo.quantidade = float(data['quantidade'])
        if 'unidade' in data:
            insumo.unidade = data['unidade']
        if 'preco' in data:
            insumo.preco = float(data['preco'])
        
        db.session.commit()
        return jsonify(insumo.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@insumo_bp.route('/insumos/<int:id>', methods=['DELETE'])
def delete_insumo(id):
    """Remove um insumo"""
    try:
        insumo = Insumo.query.get_or_404(id)
        db.session.delete(insumo)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400