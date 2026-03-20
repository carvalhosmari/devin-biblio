from django.db import models


class Leitor(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    email = models.CharField(max_length=100, verbose_name='Email')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name='Endereco')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        db_table = 'leitor'
        verbose_name = 'Leitor'
        verbose_name_plural = 'Leitores'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.cpf})"
