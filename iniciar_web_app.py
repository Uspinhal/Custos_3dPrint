import os
import subprocess
import sys

def rodar_comando(comando, cwd, env=None):
    """Roda um comando no diretório especificado. Levanta SystemExit se falhar."""
    try:
        print(f"> {' '.join(comando)} (cwd={cwd})")
        subprocess.run(comando, cwd=cwd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ O comando {' '.join(comando)} falhou com código {e.returncode}")
        # tentar imprimir saída útil, se disponível
        raise SystemExit(1)

def iniciar_servidor(ambiente):
    print("🚀 Iniciando servidor Django...\n")

    # Caminho até o diretório do manage.py
    projeto_path = os.path.join(os.getcwd(), "django_app", "impressao_3d")
    manage_py = os.path.join(projeto_path, "manage.py")

    if not os.path.exists(manage_py):
        print(f"❌ manage.py não encontrado em {manage_py}")
        raise SystemExit(1)

    # Define a variável de ambiente DJANGO_ENV e escolhe arquivo .env
    if ambiente == "dev":
        os.environ["DJANGO_ENV"] = "development"
        env_file = ".env.dev"
        print(f"🌱 Ambiente de DESENVOLVIMENTO selecionado: {env_file}")
    else:
        os.environ["DJANGO_ENV"] = "production"
        env_file = ".env.prod"
        print(f"🏭 Ambiente de PRODUÇÃO LOCAL selecionado: {env_file}")

    # garantir que subprocess use o mesmo ambiente (cópia é mais seguro)
    subprocess_env = os.environ.copy()

    # Mostrar qual banco será usado (lê do .env no projeto)
    db_name = ""
    env_path = os.path.join(projeto_path, env_file)
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("DB_NAME"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        db_name = parts[1].strip().strip('"').strip("'")
                    break
    else:
        print(f"⚠️ Arquivo de ambiente {env_file} não encontrado em {env_path}. Verifique.")
    print(f"💾 Banco de dados configurado no .env: {db_name or '(não encontrado)'}")

    # Se DB não existir, vamos tentar criar via migrate/--run-syncdb
    db_path = os.path.join(projeto_path, db_name or "db_dev.sqlite3")

    # Rodar makemigrations e migrate (com env passado)
    print("💾 Aplicando migrations (makemigrations -> migrate)...")
    # makemigrations pode retornar "No changes detected" normalmente; tudo bem
    rodar_comando([sys.executable, manage_py, "makemigrations"], cwd=projeto_path, env=subprocess_env)

    # Se o DB não existir, tenta migrate --run-syncdb para forçar criação
    if not os.path.exists(db_path):
        print(f"🧱 Banco {db_path} não existe; tentarei criar (migrate --run-syncdb)...")
        # primeiro tente migrate normalmente (pode criar), se não criar, roda --run-syncdb
        try:
            rodar_comando([sys.executable, manage_py, "migrate"], cwd=projeto_path, env=subprocess_env)
        except SystemExit:
            # tentar com --run-syncdb
            print("⚠️ migrate padrão falhou; tentando migrate --run-syncdb para criar tabelas básicas...")
            rodar_comando([sys.executable, manage_py, "migrate", "--run-syncdb"], cwd=projeto_path, env=subprocess_env)
    else:
        # DB já existe: só garantir que migrate rode
        rodar_comando([sys.executable, manage_py, "migrate"], cwd=projeto_path, env=subprocess_env)

    # Comando para rodar o servidor
    if ambiente == "dev":
        comando = [sys.executable, manage_py, "runserver"]
    else:
        comando = [sys.executable, manage_py, "runserver", "0.0.0.0:8000"]

    # Executa o comando no diretório do projeto (passando env)
    print("🚀 Iniciando servidor Django...")
    subprocess.run(comando, cwd=projeto_path, env=subprocess_env)

if __name__ == "__main__":
    print("Selecione o ambiente:\n1️⃣  Desenvolvimento\n2️⃣  Produção Local\n")
    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        iniciar_servidor("dev")
    elif escolha == "2":
        iniciar_servidor("prod")
    else:
        print("❌ Opção inválida! Encerrando.")
