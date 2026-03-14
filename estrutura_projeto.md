# Estrutura do Projeto Bibliomania

## Tabela de Arquivos

| Arquivo | Categoria | Funcao |
|---|---|---|
| `manage.py` | Back-end | Utilitario de linha de comando do Django para tarefas administrativas (runserver, migrate, etc.) |
| `requirements.txt` | Back-end | Lista de dependencias Python do projeto (Django, FastAPI, psycopg2, uvicorn, etc.) |
| `.env` | Back-end | Variaveis de ambiente com credenciais do banco de dados (Supabase) |
| `.env.example` | Back-end | Modelo de variaveis de ambiente sem valores sensiveis, para referencia |
| `.gitignore` | Back-end | Define arquivos e pastas ignorados pelo Git (venv, __pycache__, .env, db.sqlite3, etc.) |
| `README.md` | Back-end | Documentacao geral do projeto com instrucoes de instalacao, arquitetura e endpoints |
| `leitor_passo_a_passo.txt` | Back-end | Documentacao do passo a passo da implementacao do componente Leitor |
| `emprestimo_passo_a_passo.txt` | Back-end | Documentacao do passo a passo da implementacao do componente Emprestimo |
| **bibliomania/** | | |
| `bibliomania/__init__.py` | Back-end | Arquivo de inicializacao do pacote Python do projeto Django |
| `bibliomania/settings.py` | Back-end | Configuracoes do Django: apps instalados, banco de dados (PostgreSQL/SQLite), templates, middleware |
| `bibliomania/urls.py` | Back-end | Roteamento principal do Django: mapeia URLs para os apps leitor e emprestimo |
| `bibliomania/wsgi.py` | Back-end | Ponto de entrada WSGI para deploy em servidores de producao |
| `bibliomania/asgi.py` | Back-end | Ponto de entrada ASGI para deploy assincrono em servidores de producao |
| **leitor/** | | |
| `leitor/__init__.py` | Back-end | Arquivo de inicializacao do pacote Python do app Leitor |
| `leitor/apps.py` | Back-end | Configuracao do app Django Leitor (classe LeitorConfig) |
| `leitor/models.py` | Back-end | Modelo de dados Leitor com campos: nome, email, telefone, endereco, data_cadastro, ativo |
| `leitor/interfaces.py` | Back-end | Interfaces abstratas ILeitorRepository e ILeitorService que definem os contratos de acesso a dados e logica de negocio |
| `leitor/repositories.py` | Back-end | Implementacao concreta do ILeitorRepository usando Django ORM para operacoes CRUD no banco |
| `leitor/services.py` | Back-end | Implementacao concreta do ILeitorService com regras de negocio (validacao de email unico, historico de emprestimos) |
| `leitor/container.py` | Back-end | Container de injecao de dependencia (Singleton) que instancia e fornece o repositorio e servico do Leitor |
| `leitor/forms.py` | Back-end | Formularios Django (CadastrarLeitorForm, EditarLeitorForm) para validacao de dados de entrada |
| `leitor/views.py` | Back-end | Views Django que processam requisicoes HTTP e renderizam templates (listar, cadastrar, editar, perfil) |
| `leitor/urls.py` | Back-end | Rotas do app Leitor: /leitor/, /leitor/cadastrar/, /leitor/<id>/editar/, /leitor/<id>/perfil/ |
| `leitor/admin.py` | Back-end | Registro do modelo Leitor no Django Admin com configuracao de exibicao e filtros |
| `leitor/api.py` | API | Endpoints REST FastAPI para Leitor: GET/POST /api/leitores, GET/PUT /api/leitores/{id}, GET /api/leitores/{id}/historico |
| `leitor/tests.py` | Back-end | Arquivo de testes unitarios do app Leitor (placeholder) |
| `leitor/migrations/__init__.py` | Back-end | Arquivo de inicializacao do pacote de migracoes do Leitor |
| `leitor/migrations/0001_initial.py` | Back-end | Migracao inicial que cria a tabela leitor no banco de dados |
| **emprestimo/** | | |
| `emprestimo/__init__.py` | Back-end | Arquivo de inicializacao do pacote Python do app Emprestimo |
| `emprestimo/apps.py` | Back-end | Configuracao do app Django Emprestimo (classe EmprestimoConfig) |
| `emprestimo/models.py` | Back-end | Modelo de dados Emprestimo com FK para Leitor e Livro, campos: data_emprestimo, data_devolucao, data_limite, status, renovacoes |
| `emprestimo/interfaces.py` | Back-end | Interfaces abstratas IEmprestimoRepository e IEmprestimoService que definem os contratos de acesso a dados e logica de negocio |
| `emprestimo/repositories.py` | Back-end | Implementacao concreta do IEmprestimoRepository usando Django ORM para operacoes CRUD no banco |
| `emprestimo/services.py` | Back-end | Implementacao concreta do IEmprestimoService com regras de negocio (prazo 7 dias, max 2 renovacoes, multa R$1/dia, validacao de leitor e livro) |
| `emprestimo/container.py` | Back-end | Container de injecao de dependencia (Singleton) que instancia e fornece o repositorio e servico do Emprestimo, injetando tambem o repositorio do Leitor |
| `emprestimo/forms.py` | Back-end | Formulario Django (RegistrarEmprestimoForm) com dropdowns dinamicos de leitores ativos e livros disponiveis |
| `emprestimo/views.py` | Back-end | Views Django que processam requisicoes HTTP e renderizam templates (listar, registrar, devolver, renovar, detalhes) |
| `emprestimo/urls.py` | Back-end | Rotas do app Emprestimo: /emprestimo/, /emprestimo/registrar/, /emprestimo/<id>/devolver/, /emprestimo/<id>/renovar/, /emprestimo/<id>/detalhes/ |
| `emprestimo/admin.py` | Back-end | Registro do modelo Emprestimo no Django Admin com configuracao de exibicao e filtros |
| `emprestimo/api.py` | API | Endpoints REST FastAPI para Emprestimo: GET/POST /api/emprestimos, POST devolver/renovar, GET prazo |
| `emprestimo/tests.py` | Back-end | Arquivo de testes unitarios do app Emprestimo (placeholder) |
| `emprestimo/migrations/__init__.py` | Back-end | Arquivo de inicializacao do pacote de migracoes do Emprestimo |
| `emprestimo/migrations/0001_initial.py` | Back-end | Migracao inicial que cria a tabela emprestimo no banco de dados com FKs para leitor e livro |
| **livro/** | | |
| `livro/__init__.py` | Back-end | Arquivo de inicializacao do pacote Python do app Livro |
| `livro/apps.py` | Back-end | Configuracao do app Django Livro (classe LivroConfig) |
| `livro/models.py` | Back-end | Modelo de dados Livro com campos: isbn, titulo, autores, pais, editora, edicao, status (disponivel/emprestado) |
| `livro/admin.py` | Back-end | Registro do modelo Livro no Django Admin com configuracao de exibicao, filtro por status e busca por titulo/isbn/autores |
| `livro/views.py` | Back-end | Arquivo de views do app Livro (placeholder, a ser implementado no proximo componente) |
| `livro/tests.py` | Back-end | Arquivo de testes unitarios do app Livro (placeholder) |
| `livro/migrations/__init__.py` | Back-end | Arquivo de inicializacao do pacote de migracoes do Livro |
| `livro/migrations/0001_initial.py` | Back-end | Migracao inicial que cria a tabela livro no banco de dados |
| **templates/** | | |
| `templates/base.html` | Front-end | Template base com layout HTML, navbar Bootstrap 5, links de navegacao (Leitores, Emprestimos) e bloco de mensagens |
| `templates/leitor/listar.html` | Front-end | Template que exibe a tabela de leitores cadastrados com acoes (editar, perfil) |
| `templates/leitor/cadastrar.html` | Front-end | Template com formulario para cadastro de novo leitor |
| `templates/leitor/editar.html` | Front-end | Template com formulario para edicao dos dados de um leitor |
| `templates/leitor/perfil.html` | Front-end | Template que exibe o perfil do leitor com seus dados e historico de emprestimos |
| `templates/emprestimo/listar.html` | Front-end | Template que exibe a tabela de emprestimos ativos com acoes (detalhes, devolver, renovar) |
| `templates/emprestimo/registrar.html` | Front-end | Template com formulario para registrar novo emprestimo (selecao de leitor e livro) |
| `templates/emprestimo/detalhes.html` | Front-end | Template que exibe detalhes de um emprestimo com informacoes de prazo, renovacoes e multa |

## Injecao de Dependencia

### Como foi implementada

A injecao de dependencia no projeto Bibliomania segue o padrao **Interface + Container (Singleton)**, aplicado nos componentes Leitor e Emprestimo. O objetivo e evitar acoplamento direto entre as camadas, permitindo que a logica de negocio (Service) nao dependa diretamente da implementacao concreta de acesso a dados (Repository).

### Estrutura por componente

Cada componente possui tres arquivos que formam o mecanismo de injecao de dependencia:

1. **`interfaces.py`** - Define as interfaces abstratas (classes ABC):
   - `IRepository` - Contrato para a camada de acesso a dados (criar, atualizar, listar, buscar)
   - `IService` - Contrato para a camada de logica de negocio (regras de negocio, validacoes)

2. **`repositories.py`** - Implementacao concreta do `IRepository`:
   - Implementa todos os metodos abstratos usando Django ORM
   - E a unica camada que conhece o banco de dados diretamente

3. **`services.py`** - Implementacao concreta do `IService`:
   - Recebe o repositorio via **construtor** (injecao por construtor)
   - Nunca instancia o repositorio diretamente
   - Depende apenas da interface abstrata, nao da implementacao concreta

4. **`container.py`** - Container de injecao de dependencia:
   - Implementa o padrao **Singleton** com `@classmethod`
   - Responsavel por instanciar e conectar as dependencias
   - Fornece metodos `get_repository()` e `get_service()`
   - Possui metodo `reset()` para facilitar testes

### Fluxo de funcionamento

```
Views/API  -->  Container.get_service()  -->  Service(repository)  -->  Repository  -->  Django ORM  -->  Banco de Dados
```

1. A **View** (ou endpoint da API) solicita o servico ao **Container**:
   ```python
   service = EmprestimoContainer.get_service()
   ```

2. O **Container** verifica se ja existe uma instancia (Singleton). Se nao, cria o **Repository** e injeta no **Service**:
   ```python
   cls._service_instance = EmprestimoService(
       emprestimo_repository=cls.get_repository(),
       leitor_repository=LeitorContainer.get_repository(),
   )
   ```

3. O **Service** recebe os repositorios pelo construtor e os armazena:
   ```python
   class EmprestimoService(IEmprestimoService):
       def __init__(
           self,
           emprestimo_repository: IEmprestimoRepository,
           leitor_repository: ILeitorRepository,
       ):
           self._emprestimo_repo = emprestimo_repository
           self._leitor_repo = leitor_repository
   ```

4. O **Service** utiliza os repositorios apenas pelas interfaces abstratas (`IEmprestimoRepository`, `ILeitorRepository`), sem conhecer as classes concretas.

### Exemplo concreto: Componente Emprestimo

O componente Emprestimo demonstra a injecao de dependencia com **multiplas dependencias**, pois depende tanto do seu proprio repositorio quanto do repositorio do Leitor:

```
emprestimo/interfaces.py       -> Define IEmprestimoRepository e IEmprestimoService (contratos abstratos)
emprestimo/repositories.py     -> EmprestimoRepository implementa IEmprestimoRepository (acesso ao banco via Django ORM)
emprestimo/services.py         -> EmprestimoService implementa IEmprestimoService, recebe IEmprestimoRepository e ILeitorRepository no construtor
emprestimo/container.py        -> EmprestimoContainer cria EmprestimoRepository e injeta junto com LeitorContainer.get_repository() em EmprestimoService
emprestimo/views.py            -> Usa EmprestimoContainer.get_service() para obter o servico pronto para uso
emprestimo/api.py              -> Usa EmprestimoContainer.get_service() para obter o servico pronto para uso
```

### Exemplo concreto: Componente Leitor

```
leitor/interfaces.py       -> Define ILeitorRepository e ILeitorService (contratos abstratos)
leitor/repositories.py     -> LeitorRepository implementa ILeitorRepository (acesso ao banco via Django ORM)
leitor/services.py         -> LeitorService implementa ILeitorService, recebe ILeitorRepository no construtor
leitor/container.py        -> LeitorContainer cria LeitorRepository e injeta em LeitorService (Singleton)
leitor/views.py            -> Usa LeitorContainer.get_service() para obter o servico pronto para uso
leitor/api.py              -> Usa LeitorContainer.get_service() para obter o servico pronto para uso
```

### Beneficios desta abordagem

- **Desacoplamento**: O Service nao conhece a implementacao concreta do Repository
- **Testabilidade**: E possivel substituir o Repository por um mock nos testes (via `Container.reset()`)
- **Principio da Inversao de Dependencia (DIP)**: Modulos de alto nivel (Service) dependem de abstracoes (interfaces), nao de implementacoes concretas
- **Singleton**: Garante uma unica instancia por componente, evitando criacao desnecessaria de objetos
- **Composicao entre componentes**: O EmprestimoContainer reutiliza o LeitorContainer para obter o repositorio de leitores, demonstrando como a DI facilita a integracao entre componentes sem acoplamento direto
