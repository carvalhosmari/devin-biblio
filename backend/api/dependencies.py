"""
Dependency Injection Container
Configura e fornece as dependencias (services) para os routers da API.
Utiliza o mecanismo de injecao de dependencia do FastAPI (Depends).

Cada service implementa sua respectiva interface (ILeitor, ILivro, IEmprestimo),
permitindo a substituicao de implementacoes sem alterar os routers.
"""
