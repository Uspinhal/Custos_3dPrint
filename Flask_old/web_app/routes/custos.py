from flask import Blueprint, request, jsonify
from web_app.models.materia_prima import MateriaPrima
from web_app.models.equipamento import Equipamento
from web_app.models.insumo import Insumo

custos_bp = Blueprint('custos', __name__)

@custos_bp.route('/calcular-custos', methods=['POST'])
def calcular_custos():
    """Calcula os custos de uma impressão usando a lógica original"""
    data = request.get_json()
    
    required_fields = ['equipamento_id', 'materia_prima_id', 'quantidade_utilizada', 'tempo_impressao']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    try:
        # Buscar equipamento
        equipamento = Equipamento.query.get(data['equipamento_id'])
        if not equipamento:
            return jsonify({'error': 'Equipamento não encontrado'}), 404
        
        # Buscar matéria-prima
        materia_prima = MateriaPrima.query.get(data['materia_prima_id'])
        if not materia_prima:
            return jsonify({'error': 'Matéria-prima não encontrada'}), 404
        
        # Buscar custo de energia
        energia = Insumo.query.filter_by(nome='Energia').first()
        if not energia:
            return jsonify({'error': 'Insumo "Energia" não encontrado. Cadastre primeiro.'}), 404
        
        quantidade_utilizada = float(data['quantidade_utilizada'])
        tempo_impressao = float(data['tempo_impressao'])
        
        # Calcular custo da matéria-prima (preço por kg * quantidade em gramas / 1000)
        custo_materia_prima = materia_prima.preco * (quantidade_utilizada / 1000)
        
        # Calcular custo de energia (potência em kW * tempo em horas * preço por kWh)
        consumo_energia = (equipamento.potencia / 1000) * (tempo_impressao / 60)
        custo_energia = consumo_energia * energia.preco
        
        # Custo total
        custo_total = custo_materia_prima + custo_energia
        
        resultado = {
            'equipamento': equipamento.to_dict(),
            'materia_prima': materia_prima.to_dict(),
            'quantidade_utilizada': quantidade_utilizada,
            'tempo_impressao': tempo_impressao,
            'custo_materia_prima': round(custo_materia_prima, 2),
            'custo_energia': round(custo_energia, 2),
            'custo_total': round(custo_total, 2),
            'detalhes': {
                'consumo_energia_kwh': round(consumo_energia, 4),
                'preco_energia_kwh': energia.preco
            }
        }
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400