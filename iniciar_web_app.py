import os
import subprocess
import sys

def iniciar_servidor():
    print("🚀 Iniciando servidor Django...\n")

    # Caminho correto para a pasta do manage.py
    projeto_path = os.path.join("django_app", "impressao_3d")  # não precisa adicionar de novo
    manage_py = os.path.join(projeto_path, "manage.py")

    print("Caminho do projeto:", projeto_path)
    print("Caminho do manage.py:", manage_py)

    # Rodar servidor Django
    comando = [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]
    subprocess.run(comando, cwd=projeto_path)  # define cwd como a pasta do manage.py

if __name__ == "__main__":
    iniciar_servidor()