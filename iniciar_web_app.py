import os
import subprocess
import sys

def iniciar_servidor(ambiente="dev"):
    print("🚀 Iniciando servidor Django...\n")

    # Caminho até o diretório do manage.py
    projeto_path = os.path.join("django_app", "impressao_3d")
    manage_py = os.path.join(projeto_path, "manage.py")

    # Define a variável de ambiente DJANGO_ENV
    if ambiente == "dev":
        os.environ["DJANGO_ENV"] = "development"
        print("🌱 Ambiente de desenvolvimento selecionado")
        comando = [sys.executable, manage_py, "runserver"]
    else:
        os.environ["DJANGO_ENV"] = "production"
        print("🏭 Ambiente de PRODUÇÃO LOCAL selecionado")
        comando = [sys.executable, manage_py, "runserver", "0.0.0.0:8000"]

    # Executa o comando no diretório do projeto
    subprocess.run(comando, cwd=projeto_path)


if __name__ == "__main__":
    print("Selecione o ambiente:\n1️⃣  Desenvolvimento\n2️⃣  Produção Local\n")
    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        iniciar_servidor("dev")
    elif escolha == "2":
        iniciar_servidor("prod")
    else:
        print("❌ Opção inválida! Encerrando.")