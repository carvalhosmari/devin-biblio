from django import forms

from leitor.models import Leitor
from livro.models import Livro


class RegistrarEmprestimoForm(forms.Form):
    id_leitor = forms.ModelChoiceField(
        queryset=Leitor.objects.filter(ativo=True),
        label='Leitor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um leitor',
    )
    id_livro = forms.ModelChoiceField(
        queryset=Livro.objects.filter(status='disponivel'),
        label='Livro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um livro',
    )
