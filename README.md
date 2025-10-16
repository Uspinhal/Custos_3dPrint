# 🧪 Sistema de Gestão de Estoque – Impressão 3D

Aplicação web desenvolvida em **Django** para controle de matérias-primas, marcas e equipamentos utilizados em processos de **impressão 3D**.  
O sistema permite cadastrar, listar, editar e excluir registros de forma simples e intuitiva — incluindo a criação dinâmica de novas marcas diretamente no formulário de matérias-primas via **AJAX**, sem recarregar a página.

---

## 🚀 Funcionalidades Principais

- 🧱 **Cadastro de matérias-primas**
  - Nome, marca, tipo, quantidade e outras informações relevantes.
- 🏷️ **Cadastro de marcas**
  - Pode ser feito diretamente na tela de matérias-primas, através de um modal AJAX.
- 🧰 **Gestão de equipamentos**
  - Cadastro, listagem e edição de impressoras e acessórios.
- 📦 **Controle de estoque**
  - Consulta rápida e organização por marca ou tipo de material.
- 🖥️ **Interface responsiva**
  - Construída com **Bootstrap 5**.
- 🔐 **Painel administrativo Django**
  - Acesso completo para gerenciar todos os registros do sistema.

---

## 🏗️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Django 5+](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [JavaScript (AJAX / Fetch API)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- HTML5 / CSS3

---

## ⚙️ Como Rodar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário (opcional, para o admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

7. **Acesse no navegador:**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🧩 Estrutura Básica do Projeto

```
estoque/
├── models.py
├── views.py
├── urls.py
├── templates/
│   ├── estoque/
│   │   ├── lista.html
│   │   └── form.html
│   └── base.html
└── static/
    └── js/
        └── marca_ajax.js
```

---

## 💬 Observações

- O botão **"Nova Marca"** abre um modal que permite cadastrar uma nova marca sem sair da página.
- O sistema está preparado para uso com o **Django Admin** e também via **frontend customizado**.
- O código JavaScript deve estar incluído **dentro do `<body>`** ou através do bloco `{% block scripts %}` definido no `base.html`.

---

## 🧠 Próximos Passos

- Adicionar autenticação completa de usuários.
- Criar dashboards com gráficos de consumo de materiais.
- Implementar relatórios exportáveis (PDF / Excel).

---

## 👨‍💻 Autor

**Rodrigo [@Uspinhal]**  
Engenheiro, nerd e apaixonado por tecnologia e cultura POP.  


---

## 🪪 Licença

Este projeto está sob a licença MIT — sinta-se livre para usar, estudar e adaptar.
