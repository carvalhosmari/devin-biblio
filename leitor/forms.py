from django import forms

from leitor.models import Leitor


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ['nome', 'cpf', 'email', 'telefone', 'endereco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereco completo',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
