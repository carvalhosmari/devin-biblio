# Estrutura do Projeto Bibliomania

## Tabela de Arquivos

| Arquivo | Categoria | Funcao |
|---|---|---|
| **bibliomania/** | | |
| `bibliomania/settings.py` | Lucas | Configuracoes do Django: apps instalados, banco de dados (PostgreSQL/SQLite), templates, middleware |
| `bibliomania/urls.py` | Mari | Roteamento principal do Django: mapeia URLs para os apps leitor, emprestimo e livro |
| **livro/** | | |
| `livro/interfaces.py` | Lucas | Interfaces abstratas ILivroRepository e ILivroService que definem os contratos de acesso a dados e logica de negocio |
| `livro/repositories.py` | Mari | Implementacao concreta do ILivroRepository usando Django ORM, com pesquisa por Q objects em multiplos campos |
| `livro/services.py` | Lucas | Implementacao concreta do ILivroService com integracao Google Books API, validacao ISBN-10/13 e controle de estoque |
| `livro/container.py` | Lucas | Container de injecao de dependencia (Singleton) que instancia e fornece o repositorio e servico do Livro |
| `livro/forms.py` | Marcela | Formularios Django (CadastrarLivroForm, EditarLivroForm, PesquisarLivroForm) para validacao de dados |
| `livro/views.py` | Mari | Views Django que processam requisicoes HTTP e renderizam templates (listar, cadastrar, editar, detalhes) |
| `livro/urls.py` | Mari | Rotas do app Livro: /livro/, /livro/cadastrar/, /livro/<id>/editar/, /livro/isbn/<isbn>/detalhes/ |
| `livro/api.py` | Mari | Endpoints REST FastAPI para Livro: GET/POST /api/livros, PUT /api/livros/{id}, GET isbn/{isbn}, POST estoque, GET validar |
| **templates/** | | |
| `templates/base.html` | Marcela | Template base com layout HTML, navbar Bootstrap 5, links de navegacao e bloco de mensagens |
| `templates/emprestimo/listar.html` | Marcela | Template que exibe a tabela de emprestimos ativos com acoes (detalhes, devolver, renovar) |
| `templates/livro/listar.html` | Marcela | Template que exibe o acervo de livros agrupados por ISBN com pesquisa e contagem de exemplares |
| `templates/livro/cadastrar.html` | Marcela | Template com formulario para cadastrar livros via ISBN (com integracao Google Books API) |
| `templates/livro/editar.html` | Marcela | Template com formulario para edicao dos dados de um exemplar de livro |
| `templates/livro/detalhes.html` | Marcela | Template que exibe detalhes do livro por ISBN com painel de estoque (total, disponiveis, emprestados) |

