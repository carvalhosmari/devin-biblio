from django import forms

from leitor.models import Leitor
from livro.models import Livro


class RegistrarEmprestimoForm(forms.Form):
    id_leitor = forms.ModelChoiceField(
        queryset=Leitor.objects.none(),
        label='Leitor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um leitor',
    )
    id_livro = forms.ModelChoiceField(
        queryset=Livro.objects.none(),
        label='Livro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Selecione um livro',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_leitor'].queryset = Leitor.objects.filter(ativo=True)
        self.fields['id_livro'].queryset = Livro.objects.filter(status='disponivel')
