#!/usr/bin/env python3
"""
Script para iniciar a aplicação web do Sistema de Gestão Make It Real 3D
"""
"""
import os
import sys

def main():
    
    print("🎯 Iniciando Sistema Web de Gestão Make It Real 3D...")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('web_app'):
        print("❌ Erro: Execute este script a partir da pasta raiz do projeto")
        print("   Certifique-se de estar na pasta 'Custos_3dPrint'")
        return
    
    # Verificar dependências
    try:
        import flask
        print("✅ Flask encontrado")
    except ImportError:
        print("❌ Flask não encontrado. Instale as dependências:")
        print("   pip install -r requirements.txt")
        return
    
    # Importar e executar a aplicação
    try:
        from web_app.app import main as run_app
        run_app()
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        print("   Verifique se todas as dependências estão instaladas")

if __name__ == '__main__':
    main()
"""

from flask import app
from web_app.app import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)