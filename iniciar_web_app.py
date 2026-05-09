import os
import subprocess
import sys

def rodar_comando(comando, cwd, env=None):
    try:
        print(f"> {' '.join(comando)} (cwd={cwd})")
        subprocess.run(comando, cwd=cwd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ O comando {' '.join(comando)} falhou com código {e.returncode}")
        raise SystemExit(1)

def iniciar_servidor(ambiente):
    print("🚀 Iniciando servidor Django...\n")

    projeto_path = os.path.join(os.getcwd(), "django_app", "impressao_3d")
    manage_py = os.path.join(projeto_path, "manage.py")

    if not os.path.exists(manage_py):
        print(f"❌ manage.py não encontrado em {manage_py}")
        raise SystemExit(1)

    if ambiente == "dev":
        os.environ["DJANGO_ENV"] = "development"
        env_file = ".env.dev"
        print(f"🌱 Ambiente de DESENVOLVIMENTO selecionado: {env_file}")
    else:
        os.environ["DJANGO_ENV"] = "production"
        env_file = ".env.prod"
        print(f"🏭 Ambiente de PRODUÇÃO selecionado: {env_file}")

    subprocess_env = os.environ.copy()

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
        print(f"⚠️ Arquivo {env_file} não encontrado em {env_path}. Verifique.")

    print(f"💾 Banco de dados: {db_name or '(não encontrado)'}")

    db_path = os.path.join(projeto_path, db_name or "db_dev.sqlite3")

    print("💾 Aplicando migrations...")
    rodar_comando([sys.executable, manage_py, "makemigrations"], cwd=projeto_path, env=subprocess_env)

    if not os.path.exists(db_path):
        print(f"🧱 Banco não existe, criando...")
        try:
            rodar_comando([sys.executable, manage_py, "migrate"], cwd=projeto_path, env=subprocess_env)
        except SystemExit:
            rodar_comando([sys.executable, manage_py, "migrate", "--run-syncdb"], cwd=projeto_path, env=subprocess_env)
    else:
        rodar_comando([sys.executable, manage_py, "migrate"], cwd=projeto_path, env=subprocess_env)

    # ← Aqui está a diferença principal: Gunicorn em prod, runserver em dev
    if ambiente == "dev":
        comando = [sys.executable, manage_py, "runserver", "0.0.0.0:8000"]
        print("🚀 Iniciando servidor de desenvolvimento...")
    else:
        comando = ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
        print("🚀 Iniciando Gunicorn (produção)...")
        # Coleta estáticos antes de subir em produção
        rodar_comando([sys.executable, manage_py, "collectstatic", "--noinput"], cwd=projeto_path, env=subprocess_env)

    try:
        subprocess.run(comando, cwd=projeto_path, env=subprocess_env)
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado.")

if __name__ == "__main__":
    # Aceita argumento direto: python iniciar_web_app.py dev  ou  prod
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg in ("dev", "prod"):
            iniciar_servidor(arg)
        else:
            print(f"❌ Argumento inválido: '{arg}'. Use 'dev' ou 'prod'.")
    else:
        # Fallback interativo — para uso no PC
        print("Selecione o ambiente:\n1️⃣  Desenvolvimento\n2️⃣  Produção\n")
        escolha = input("Digite 1 ou 2: ").strip()
        if escolha == "1":
            iniciar_servidor("dev")
        elif escolha == "2":
            iniciar_servidor("prod")
        else:
            print("❌ Opção inválida! Encerrando.")