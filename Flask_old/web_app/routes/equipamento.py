from flask import Blueprint, request, jsonify
from web_app.models.equipamento import Equipamento, db

equipamento_bp = Blueprint('equipamento', __name__)

@equipamento_bp.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    """Retorna todos os equipamentos cadastrados"""
    try:
        equipamentos = Equipamento.query.all()
        return jsonify([eq.to_dict() for eq in equipamentos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@equipamento_bp.route('/equipamentos', methods=['POST'])
def create_equipamento():
    """Cria um novo equipamento"""
    data = request.get_json()
    
    required_fields = ['nome', 'potencia', 'preco', 'valor_inicial', 'vida_util']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        equipamento = Equipamento(
            nome=data['nome'],
            potencia=float(data['potencia']),
            preco=float(data['preco']),
            valor_inicial=float(data['valor_inicial']),
            vida_util=float(data['vida_util'])
        )
        
        db.session.add(equipamento)
        db.session.commit()
        
        return jsonify(equipamento.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@equipamento_bp.route('/equipamentos/<int:id>', methods=['GET'])
def get_equipamento(id):
    """Retorna um equipamento específico"""
    try:
        equipamento = Equipamento.query.get_or_404(id)
        return jsonify(equipamento.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@equipamento_bp.route('/equipamentos/<int:id>', methods=['PUT'])
def update_equipamento(id):
    """Atualiza um equipamento existente"""
    equipamento = Equipamento.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome' in data:
            equipamento.nome = data['nome']
        if 'potencia' in data:
            equipamento.potencia = float(data['potencia'])
        if 'preco' in data:
            equipamento.preco = float(data['preco'])
        if 'valor_inicial' in data:
            equipamento.valor_inicial = float(data['valor_inicial'])
        if 'vida_util' in data:
            equipamento.vida_util = float(data['vida_util'])
        
        db.session.commit()
        return jsonify(equipamento.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@equipamento_bp.route('/equipamentos/<int:id>', methods=['DELETE'])
def delete_equipamento(id):
    """Remove um equipamento"""
    try:
        equipamento = Equipamento.query.get_or_404(id)
        db.session.delete(equipamento)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400