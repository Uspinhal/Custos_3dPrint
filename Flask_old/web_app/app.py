"""
Sistema Web de Gestão Make It Real 3D
Aplicação Flask para gestão interna de custos e produção
"""

import os
import sys
from flask import Flask, send_from_directory
from web_app.models.materia_prima import db
from web_app.routes.materia_prima import materia_prima_bp

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar modelos
from web_app.models.materia_prima import MateriaPrima, db
from web_app.models.equipamento import Equipamento
from web_app.models.insumo import Insumo

# Importar blueprints (rotas)
from web_app.routes.materia_prima import materia_prima_bp
from web_app.routes.equipamento import equipamento_bp
from web_app.routes.insumo import insumo_bp
from web_app.routes.custos import custos_bp

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__, 
                static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    
    # Configurações
    app.config['SECRET_KEY'] = 'make-it-real-3d-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(materia_prima_bp, url_prefix='/api')
    app.register_blueprint(equipamento_bp, url_prefix='/api')
    app.register_blueprint(insumo_bp, url_prefix='/api')
    app.register_blueprint(custos_bp, url_prefix='/api')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    # Rota para servir arquivos estáticos e SPA
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    return app

def main():
    """Função principal para executar a aplicação"""
    app = create_app()
    
    print("🎯 Sistema de Gestão Make It Real 3D")
    print("📱 Acesse: http://localhost:5000")
    print("⏹️  Para parar: Ctrl+C")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()