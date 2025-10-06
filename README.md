# Custos 3D Print

Este projeto é um sistema para gerenciamento de custos, precificação, clientes, pedidos e relatórios de uma operação de impressão 3D.

## Estrutura do Projeto
- `custos/`: Módulo de controle de custos
- `precificacao/`: Módulo de precificação
- `clientes/`: Gerenciamento de clientes
- `pedidos/`: Gerenciamento de pedidos
- `relatorios/`: Geração de relatórios
- `banco_dados/`: Conexão e manipulação do banco de dados
- `GUI/`: Interface gráfica do usuário
- `main.py`: Arquivo principal para inicialização do sistema

## Como rodar
1. Crie um ambiente virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
3. Execute o sistema:
   ```powershell
   python main.py
   ```

## Testes
Os testes estão na pasta `test/`. Para rodar:
```powershell
python -m unittest discover test
```
