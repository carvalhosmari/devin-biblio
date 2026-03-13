# Bibliomania - Sistema de Gestao de Biblioteca

Sistema para gestao de biblioteca desenvolvido com Python, Django e FastAPI.

## Arquitetura

- **Padrao**: MVT (Model-View-Template)
- **Backend**: Python com Django + FastAPI (API REST)
- **Banco de Dados**: PostgreSQL (Supabase)
- **Frontend**: Django Templates com Bootstrap 5

## Componentes

### 1. Leitor
Gerencia todas as informacoes dos leitores da biblioteca.

**Funcionalidades:**
- Cadastrar novo leitor
- Atualizar dados de leitor
- Listar todos os leitores
- Visualizar perfil e historico de emprestimos

### 2. Emprestimo
Gerencia os emprestimos de livros da biblioteca.

**Funcionalidades:**
- Registrar novo emprestimo (validando leitor ativo, livro disponivel, sem pendencias)
- Registrar devolucao (com calculo automatico de multa por atraso)
- Renovar emprestimo (maximo 2 renovacoes, +14 dias)
- Visualizar emprestimos ativos (com filtro por leitor)
- Validar prazo e calcular multa (R$1,00 por dia de atraso)

**Regras de Negocio:**
- Prazo padrao: 7 dias
- Maximo de renovacoes: 2 vezes
- Leitor deve estar ativo para realizar emprestimo
- Livro deve estar com status disponivel
- Leitor nao pode ter pendencias de devolucao
- Devolucao e emprestimo atualizam status do livro automaticamente
- Renovar encerra o emprestimo atual e cria um novo com novas datas

### 3. Livro *(a implementar - modelo minimo criado para FK)*

## Requisitos

- Python 3.12+
- PostgreSQL (Supabase)

## Instalacao

1. Clone o repositorio:
```bash
git clone https://github.com/carvalhosmari/devin-biblio.git
cd devin-biblio
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependencias:
```bash
pip install -r requirements.txt
```

4. Configure as variaveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Execute as migracoes:
```bash
python manage.py migrate
```

6. Inicie o servidor Django:
```bash
python manage.py runserver
```

7. (Opcional) Inicie a API FastAPI:
```bash
# API de Leitores
uvicorn leitor.api:api --reload --port 8001
# API de Emprestimos
uvicorn emprestimo.api:api --reload --port 8002
```

## Variaveis de Ambiente

| Variavel | Descricao |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | Modo debug (True/False) |
| `DB_NAME` | Nome do banco de dados |
| `DB_USER` | Usuario do banco de dados |
| `DB_PASSWORD` | Senha do banco de dados |
| `DB_HOST` | Host do banco de dados |
| `DB_PORT` | Porta do banco de dados |

## API REST (FastAPI)

### Leitores (porta 8001)
| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | `/api/leitores` | Listar todos os leitores |
| POST | `/api/leitores` | Cadastrar novo leitor |
| GET | `/api/leitores/{id}` | Buscar leitor por ID |
| PUT | `/api/leitores/{id}` | Atualizar leitor |
| GET | `/api/leitores/{id}/historico` | Historico do leitor |

### Emprestimos (porta 8002)
| Metodo | Endpoint | Descricao |
|---|---|---|
| GET | `/api/emprestimos` | Listar emprestimos ativos (filtro: ?id_leitor=) |
| POST | `/api/emprestimos` | Registrar novo emprestimo |
| POST | `/api/emprestimos/{id}/devolver` | Registrar devolucao |
| POST | `/api/emprestimos/{id}/renovar` | Renovar emprestimo |
| GET | `/api/emprestimos/{id}/prazo` | Verificar prazo e multa |

## Estrutura do Projeto

```
devin-biblio/
├── bibliomania/          # Configuracoes do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── leitor/               # Componente Leitor
│   ├── interfaces.py     # Interfaces abstratas (DI)
│   ├── repositories.py   # Implementacao do repositorio
│   ├── services.py       # Logica de negocio
│   ├── container.py      # Container de injecao de dependencia
│   ├── models.py         # Modelo de dados
│   ├── views.py          # Views Django (MVT)
│   ├── forms.py          # Formularios
│   ├── urls.py           # Rotas
│   ├── api.py            # Endpoints FastAPI
│   └── admin.py          # Admin Django
├── emprestimo/           # Componente Emprestimo
│   ├── interfaces.py     # Interfaces abstratas (DI)
│   ├── repositories.py   # Implementacao do repositorio
│   ├── services.py       # Logica de negocio
│   ├── container.py      # Container de injecao de dependencia
│   ├── models.py         # Modelo de dados
│   ├── views.py          # Views Django (MVT)
│   ├── forms.py          # Formularios
│   ├── urls.py           # Rotas
│   ├── api.py            # Endpoints FastAPI
│   └── admin.py          # Admin Django
├── livro/                # Componente Livro (modelo minimo para FK)
│   ├── models.py
│   └── admin.py
├── templates/            # Templates HTML
│   ├── base.html
│   ├── leitor/
│   └── emprestimo/
├── requirements.txt
├── manage.py
└── .env
```
