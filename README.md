# Bibliomania

Sistema de gestao de biblioteca desenvolvido com Django, FastAPI e React.

## Arquitetura

O projeto segue o padrao **MVT (Model-View-Template)**:

- **Model**: Django ORM — modelos de dados definidos em cada app Django (`leitor`, `livro`, `emprestimo`), responsaveis pela persistencia e regras de negocio no banco de dados.
- **View**: FastAPI — camada de API REST que expoe os endpoints para consumo do frontend. Os routers FastAPI atuam como a camada View, processando requisicoes e retornando respostas.
- **Template**: React + TypeScript + Tailwind CSS — camada de apresentacao que consome a API e renderiza a interface do usuario.

## Estrutura do Projeto

```
bibliomania/
├── backend/
│   ├── bibliomania/           # Projeto Django (settings, urls, wsgi, asgi)
│   ├── leitor/                # App Django - Componente Leitor
│   │   ├── models.py          # Model: definicao da entidade Leitor
│   │   ├── interfaces.py      # Interface ILeitor (contrato)
│   │   ├── services.py        # Service: logica de negocio (implementa ILeitor)
│   │   ├── views.py           # View Django (opcional)
│   │   └── admin.py           # Configuracao Django Admin
│   ├── livro/                 # App Django - Componente Livro
│   │   ├── models.py          # Model: definicao da entidade Livro
│   │   ├── interfaces.py      # Interface ILivro (contrato)
│   │   ├── services.py        # Service: logica de negocio (implementa ILivro)
│   │   ├── views.py           # View Django (opcional)
│   │   └── admin.py           # Configuracao Django Admin
│   ├── emprestimo/            # App Django - Componente Emprestimo
│   │   ├── models.py          # Model: definicao da entidade Emprestimo
│   │   ├── interfaces.py      # Interface IEmprestimo (contrato)
│   │   ├── services.py        # Service: logica de negocio (implementa IEmprestimo)
│   │   ├── views.py           # View Django (opcional)
│   │   └── admin.py           # Configuracao Django Admin
│   ├── api/                   # FastAPI - Camada View (API REST)
│   │   ├── main.py            # Ponto de entrada FastAPI
│   │   ├── dependencies.py    # Container de injecao de dependencia
│   │   └── routers/           # Routers por componente
│   │       ├── leitor.py      # Endpoints do Leitor
│   │       ├── livro.py       # Endpoints do Livro
│   │       └── emprestimo.py  # Endpoints do Emprestimo
│   ├── manage.py              # CLI Django
│   ├── requirements.txt       # Dependencias Python
│   └── .env.example           # Exemplo de variaveis de ambiente
├── frontend/
│   ├── src/
│   │   ├── components/        # Componentes React (Template layer)
│   │   │   ├── Leitor/        # Componente Leitor
│   │   │   ├── Livro/         # Componente Livro
│   │   │   └── Emprestimo/    # Componente Emprestimo
│   │   ├── services/          # Servicos de comunicacao com a API
│   │   ├── types/             # Tipos TypeScript
│   │   ├── pages/             # Paginas da aplicacao
│   │   ├── App.tsx            # Componente raiz
│   │   └── main.tsx           # Ponto de entrada
│   ├── .env.example           # Exemplo de variaveis de ambiente
│   ├── package.json           # Dependencias Node
│   └── tsconfig.json          # Configuracao TypeScript
├── .gitignore
└── README.md
```

## Componentes

### 1. Leitor
Gerencia as informacoes dos leitores da biblioteca (cadastro, atualizacao, listagem e historico).

### 2. Emprestimo
Gerencia os emprestimos de livros (registro, devolucao, renovacao, validacoes e multas).

### 3. Livro
Gerencia os livros da biblioteca (cadastro via ISBN com Google Books API, edicao, pesquisa e controle de estoque).

## Injecao de Dependencia

O projeto utiliza o mecanismo nativo de **Dependency Injection do FastAPI** (`Depends`) para desacoplar as camadas:

1. **Interfaces** (`interfaces.py`): Cada componente define uma interface abstrata (ABC) que estabelece o contrato do servico (ex: `ILeitor`, `ILivro`, `IEmprestimo`).
2. **Services** (`services.py`): Implementam as interfaces, contendo a logica de negocio. Acessam os Models Django para persistencia.
3. **Dependencies** (`api/dependencies.py`): Configura e fornece as instancias dos services para os routers via `Depends()`.
4. **Routers** (`api/routers/`): Recebem os services injetados como parametros, sem conhecer a implementacao concreta.

Esse mecanismo permite:
- Substituir implementacoes de servico sem alterar os routers
- Facilitar testes unitarios com mocks
- Manter baixo acoplamento entre camadas

## Como o Acoplamento e Evitado

- **Interfaces abstratas**: Os routers dependem apenas das interfaces, nao das implementacoes concretas.
- **Injecao via FastAPI Depends**: Os services sao injetados nos endpoints, evitando instanciacao direta.
- **Separacao de camadas**: Model (Django ORM), View (FastAPI routers) e Template (React) sao independentes.
- **Servicos independentes**: Cada componente (Leitor, Livro, Emprestimo) possui seu proprio service e interface, sem dependencias cruzadas diretas.

## Comunicacao entre Componentes

A comunicacao segue o fluxo:

```
[Frontend React] --HTTP--> [FastAPI Routers] --Depends--> [Services] --ORM--> [Django Models] --SQL--> [Supabase PostgreSQL]
```

1. O **Frontend** (React) faz requisicoes HTTP para a **API REST** (FastAPI).
2. Os **Routers** (FastAPI) delegam a logica para os **Services** injetados via `Depends`.
3. Os **Services** utilizam os **Models** (Django ORM) para acessar o banco de dados.
4. O **banco de dados** (Supabase PostgreSQL) persiste os dados.

## Como Executar

### Pre-requisitos
- Python 3.12+
- Node.js 18+
- npm

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Configurar variaveis de ambiente
cp .env.example .env
# Editar .env com as credenciais do banco de dados

# Executar migracoes Django
python manage.py migrate

# Iniciar servidor FastAPI
uvicorn api.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variaveis de ambiente
cp .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estara disponivel em `http://localhost:5173` e a API em `http://localhost:8000`.

## Tecnologias

- **Backend**: Python, Django 5.1, FastAPI 0.115, Uvicorn
- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Banco de Dados**: PostgreSQL (Supabase)
- **API Externa**: Google Books API (para cadastro de livros via ISBN)
