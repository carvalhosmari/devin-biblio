from django import forms

from livro.models import Livro


class CadastrarLivroForm(forms.Form):
    isbn = forms.CharField(
        max_length=25,
        label='ISBN',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 978-85-325-2898-1',
        }),
    )
    quantidade = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=1,
        label='Quantidade de exemplares',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )


class EditarLivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['isbn', 'titulo', 'autores', 'pais', 'editora', 'edicao']
        widgets = {
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autores': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'edicao': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PesquisarLivroForm(forms.Form):
    filtro = forms.CharField(
        max_length=200,
        required=False,
        label='Pesquisar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pesquisar por titulo, autor, editora ou ISBN...',
        }),
    )
