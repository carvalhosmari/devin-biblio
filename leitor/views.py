from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from leitor.container import LeitorContainer
from leitor.forms import LeitorForm


def listar_leitores(request):
    """Lista todos os leitores cadastrados."""
    service = LeitorContainer.get_service()
    leitores = service.listar_leitores()
    return render(request, 'leitor/listar.html', {'leitores': leitores})


def cadastrar_leitor(request):
    """Cadastra um novo leitor."""
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            service = LeitorContainer.get_service()
            try:
                service.cadastrar_leitor(form.cleaned_data)
                messages.success(request, 'Leitor cadastrado com sucesso!')
                return redirect('leitor:listar')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = LeitorForm()
    return render(request, 'leitor/cadastrar.html', {'form': form})


def editar_leitor(request, id_leitor):
    """Edita um leitor existente."""
    service = LeitorContainer.get_service()
    try:
        perfil = service.acessar_historico_leitor(id_leitor)
    except ValueError:
        messages.error(request, 'Leitor nao encontrado.')
        return redirect('leitor:listar')

    leitor = perfil['leitor']

    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        if form.is_valid():
            try:
                service.atualizar_leitor(id_leitor, form.cleaned_data)
                messages.success(request, 'Leitor atualizado com sucesso!')
                return redirect('leitor:listar')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = LeitorForm(instance=leitor)

    return render(request, 'leitor/editar.html', {'form': form, 'leitor': leitor})


def perfil_leitor(request, id_leitor):
    """Exibe o perfil do leitor e seu historico de emprestimos."""
    service = LeitorContainer.get_service()
    try:
        perfil = service.acessar_historico_leitor(id_leitor)
    except ValueError:
        messages.error(request, 'Leitor nao encontrado.')
        return redirect('leitor:listar')

    from emprestimo.container import EmprestimoContainer
    emprestimo_service = EmprestimoContainer.get_service()
    emprestimos = emprestimo_service.buscar_emprestimos_leitor(id_leitor)

    return render(request, 'leitor/perfil.html', {
        'leitor': perfil['leitor'],
        'emprestimos': emprestimos,
    })
