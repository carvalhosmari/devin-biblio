# Bibliomania

Sistema de gestao de biblioteca desenvolvido com Django, FastAPI e React.

## Arquitetura

O projeto segue o padrao **MVT (Model-View-Template)**:

- **Model** (`models/`): Django ORM — modelos de dados para as entidades da biblioteca (leitor, livro, emprestimo).
- **View** (`views/`): FastAPI — endpoints da API REST que processam requisicoes e retornam respostas.
- **Template** (`templates/`): React + TypeScript + Tailwind CSS — camada de apresentacao que consome a API e renderiza a interface do usuario.

## Estrutura do Projeto

```
bibliomania/
├── bibliomania/               # Projeto Django (settings, urls, wsgi, asgi)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── models/                    # M - Camada Model (Django ORM)
│   ├── __init__.py
│   ├── leitor.py              # Model Leitor
│   ├── livro.py               # Model Livro
│   └── emprestimo.py          # Model Emprestimo
├── views/                     # V - Camada View (FastAPI endpoints)
│   ├── __init__.py
│   ├── leitor.py              # Endpoints do Leitor
│   ├── livro.py               # Endpoints do Livro
│   └── emprestimo.py          # Endpoints do Emprestimo
├── templates/                 # T - Camada Template (React)
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   │   ├── Leitor/        # Componente Leitor
│   │   │   ├── Livro/         # Componente Livro
│   │   │   └── Emprestimo/    # Componente Emprestimo
│   │   ├── pages/             # Paginas da aplicacao
│   │   ├── services/          # Servicos de comunicacao com a API
│   │   ├── types/             # Tipos TypeScript
│   │   ├── App.tsx            # Componente raiz
│   │   └── main.tsx           # Ponto de entrada
│   ├── package.json           # Dependencias Node
│   ├── tsconfig.json          # Configuracao TypeScript
│   └── .env.example           # Exemplo de variaveis de ambiente
├── services/                  # Logica de negocio
│   ├── __init__.py
│   ├── interfaces/            # Contratos (ABCs)
│   │   ├── __init__.py
│   │   ├── ileitor.py         # Interface ILeitor
│   │   ├── ilivro.py          # Interface ILivro
│   │   └── iemprestimo.py     # Interface IEmprestimo
│   ├── leitor_service.py      # Implementacao ILeitor
│   ├── livro_service.py       # Implementacao ILivro
│   └── emprestimo_service.py  # Implementacao IEmprestimo
├── schemas/                   # DTOs Pydantic
│   ├── __init__.py
│   ├── leitor.py              # Schemas do Leitor
│   ├── livro.py               # Schemas do Livro
│   └── emprestimo.py          # Schemas do Emprestimo
├── dependencies.py            # Container de injecao de dependencia
├── main.py                    # Ponto de entrada FastAPI
├── manage.py                  # CLI Django
├── requirements.txt           # Dependencias Python
├── .env.example               # Exemplo de variaveis de ambiente
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

1. **Interfaces** (`services/interfaces/`): Cada componente define uma interface abstrata (ABC) que estabelece o contrato do servico (ex: `ILeitor`, `ILivro`, `IEmprestimo`).
2. **Services** (`services/*_service.py`): Implementam as interfaces, contendo a logica de negocio. Acessam os Models Django para persistencia.
3. **Dependencies** (`dependencies.py`): Configura e fornece as instancias dos services para as views via `Depends()`.
4. **Views** (`views/`): Recebem os services injetados como parametros, sem conhecer a implementacao concreta.

Esse mecanismo permite:
- Substituir implementacoes de servico sem alterar as views
- Facilitar testes unitarios com mocks
- Manter baixo acoplamento entre camadas

## Como o Acoplamento e Evitado

- **Interfaces abstratas**: As views dependem apenas das interfaces, nao das implementacoes concretas.
- **Injecao via FastAPI Depends**: Os services sao injetados nos endpoints, evitando instanciacao direta.
- **Separacao de camadas**: Model (`models/`), View (`views/`) e Template (`templates/`) sao diretorios independentes no mesmo projeto.
- **Servicos independentes**: Cada componente (Leitor, Livro, Emprestimo) possui seu proprio service e interface, sem dependencias cruzadas diretas.

## Comunicacao entre Componentes

A comunicacao segue o fluxo:

```
[Templates/React] --HTTP--> [Views/FastAPI] --Depends--> [Services] --ORM--> [Models/Django] --SQL--> [Supabase PostgreSQL]
```

1. Os **Templates** (React) fazem requisicoes HTTP para as **Views** (FastAPI).
2. As **Views** (FastAPI) delegam a logica para os **Services** injetados via `Depends`.
3. Os **Services** utilizam os **Models** (Django ORM) para acessar o banco de dados.
4. O **banco de dados** (Supabase PostgreSQL) persiste os dados.

## Como Executar

### Pre-requisitos
- Python 3.12+
- Node.js 18+
- npm

### Backend (Models + Views + Services)

```bash
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
uvicorn main:app --reload --port 8000
```

### Templates (Frontend React)

```bash
cd templates

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
