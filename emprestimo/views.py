from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from emprestimo.container import EmprestimoContainer
from emprestimo.forms import RegistrarEmprestimoForm


def listar_emprestimos(request):
    """Lista emprestimos ativos, opcionalmente filtrados por leitor."""
    service = EmprestimoContainer.get_service()
    id_leitor = request.GET.get('id_leitor')
    if id_leitor:
        try:
            id_leitor = int(id_leitor)
        except (ValueError, TypeError):
            id_leitor = None

    emprestimos = service.visualizar_emprestimos_ativos(id_leitor)

    # Calcular informacoes de prazo para cada emprestimo
    emprestimos_info = []
    for emp in emprestimos:
        try:
            prazo_info = service.validar_prazo(emp.id)
            emprestimos_info.append({
                'emprestimo': emp,
                'atrasado': prazo_info['atrasado'],
                'dias_restantes': prazo_info['dias_restantes'],
                'dias_atraso': prazo_info['dias_atraso'],
                'multa': prazo_info['multa'],
            })
        except ValueError:
            emprestimos_info.append({
                'emprestimo': emp,
                'atrasado': False,
                'dias_restantes': 0,
                'dias_atraso': 0,
                'multa': 0,
            })

    return render(request, 'emprestimo/listar.html', {
        'emprestimos_info': emprestimos_info,
        'filtro_leitor': id_leitor,
    })


def registrar_emprestimo(request):
    """Registra um novo emprestimo."""
    if request.method == 'POST':
        form = RegistrarEmprestimoForm(request.POST)
        if form.is_valid():
            service = EmprestimoContainer.get_service()
            try:
                id_leitor = form.cleaned_data['id_leitor'].id
                id_livro = form.cleaned_data['id_livro'].id
                service.registrar_emprestimo(id_leitor, id_livro)
                messages.success(request, 'Emprestimo registrado com sucesso!')
                return redirect('emprestimo:listar')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = RegistrarEmprestimoForm()
    return render(request, 'emprestimo/registrar.html', {'form': form})


@require_POST
def registrar_devolucao(request, id_emprestimo):
    """Registra a devolucao de um livro."""
    service = EmprestimoContainer.get_service()
    try:
        resultado = service.registrar_devolucao(id_emprestimo)
        multa = resultado['multa']
        if multa > 0:
            messages.warning(
                request,
                f'Livro devolvido com atraso. Multa: R$ {multa:.2f}'
            )
        else:
            messages.success(request, 'Devolucao registrada com sucesso!')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('emprestimo:listar')


@require_POST
def renovar_emprestimo(request, id_emprestimo):
    """Renova o emprestimo por mais 14 dias."""
    service = EmprestimoContainer.get_service()
    try:
        service.renovar_emprestimo(id_emprestimo)
        messages.success(request, 'Emprestimo renovado com sucesso!')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('emprestimo:listar')


def detalhes_emprestimo(request, id_emprestimo):
    """Exibe detalhes de um emprestimo com informacoes de prazo."""
    service = EmprestimoContainer.get_service()
    try:
        prazo_info = service.validar_prazo(id_emprestimo)
    except ValueError:
        messages.error(request, 'Emprestimo nao encontrado.')
        return redirect('emprestimo:listar')

    return render(request, 'emprestimo/detalhes.html', {
        'emprestimo': prazo_info['emprestimo'],
        'atrasado': prazo_info['atrasado'],
        'dias_restantes': prazo_info['dias_restantes'],
        'dias_atraso': prazo_info['dias_atraso'],
        'multa': prazo_info['multa'],
    })
