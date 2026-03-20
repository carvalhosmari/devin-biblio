from django.shortcuts import render, redirect
from django.contrib import messages

from livro.container import LivroContainer
from livro.forms import CadastrarLivroForm, EditarLivroForm, PesquisarLivroForm


def listar_livros(request):
    """Lista todos os livros com opcao de pesquisa."""
    service = LivroContainer.get_service()
    form = PesquisarLivroForm(request.GET or None)
    filtro = ''

    if form.is_valid():
        filtro = form.cleaned_data.get('filtro', '')

    if filtro:
        livros = service.pesquisar_livros(filtro)
    else:
        livros = service.listar_livros()

    # Agrupar livros por ISBN
    isbn_groups = {}
    for livro in livros:
        if livro.isbn not in isbn_groups:
            isbn_groups[livro.isbn] = {
                'isbn': livro.isbn,
                'titulo': livro.titulo,
                'autores': livro.autores,
                'editora': livro.editora,
                'total': 0,
                'disponiveis': 0,
                'exemplares': [],
            }
        isbn_groups[livro.isbn]['total'] += 1
        if livro.status == 'disponivel':
            isbn_groups[livro.isbn]['disponiveis'] += 1
        isbn_groups[livro.isbn]['exemplares'].append(livro)

    return render(request, 'livro/listar.html', {
        'isbn_groups': isbn_groups.values(),
        'form': form,
        'filtro': filtro,
    })


def cadastrar_livro(request):
    """Cadastra livro(s) a partir do ISBN usando a API Google Books."""
    if request.method == 'POST':
        form = CadastrarLivroForm(request.POST)
        if form.is_valid():
            service = LivroContainer.get_service()
            try:
                isbn = form.cleaned_data['isbn']
                quantidade = form.cleaned_data['quantidade']
                livros = service.cadastrar_livro(isbn, quantidade)
                titulo = livros[0].titulo if livros else isbn
                messages.success(
                    request,
                    f'{quantidade} exemplar(es) de "{titulo}" cadastrado(s) com sucesso!'
                )
                return redirect('livro:listar')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CadastrarLivroForm()
    return render(request, 'livro/cadastrar.html', {'form': form})


def editar_livro(request, id_livro):
    """Edita as informacoes de um livro."""
    service = LivroContainer.get_service()
    livro = service.buscar_livro_por_id(id_livro)
    if not livro:
        messages.error(request, 'Livro nao encontrado.')
        return redirect('livro:listar')

    if request.method == 'POST':
        form = EditarLivroForm(request.POST, instance=livro)
        if form.is_valid():
            try:
                service.editar_livro(id_livro, form.cleaned_data)
                messages.success(request, 'Livro atualizado com sucesso!')
                return redirect('livro:listar')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = EditarLivroForm(instance=livro)

    return render(request, 'livro/editar.html', {'form': form, 'livro': livro})


def detalhes_livro(request, isbn):
    """Visualiza detalhes de livros agrupados por ISBN."""
    service = LivroContainer.get_service()
    try:
        detalhes = service.visualizar_detalhes_livro(isbn)
    except ValueError:
        messages.error(request, 'Nenhum livro encontrado com este ISBN.')
        return redirect('livro:listar')

    return render(request, 'livro/detalhes.html', {'detalhes': detalhes})
