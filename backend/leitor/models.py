"""
Model: Leitor (Reader)
Componente responsavel pelo gerenciamento dos leitores da biblioteca.
"""

from django.db import models


class Leitor(models.Model):
    """Modelo de dados do Leitor."""

    nome = models.CharField(max_length=200, verbose_name="Nome completo")
    email = models.CharField(max_length=100, verbose_name="Email")
    telefone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Telefone"
    )
    endereco = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Endereco"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Status ativo")

    class Meta:
        db_table = "leitor"
        verbose_name = "Leitor"
        verbose_name_plural = "Leitores"

    def __str__(self):
        return self.nome
