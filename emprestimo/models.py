from django.db import models

from leitor.models import Leitor
from livro.models import Livro


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('devolvido', 'Devolvido'),
        ('atrasado', 'Atrasado'),
        ('renovado', 'Renovado'),
    ]

    id_leitor = models.ForeignKey(
        Leitor,
        on_delete=models.CASCADE,
        related_name='emprestimos',
        verbose_name='Leitor',
    )
    id_livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='emprestimos',
        verbose_name='Livro',
    )
    data_emprestimo = models.DateTimeField(auto_now_add=True, verbose_name='Data do emprestimo')
    data_devolucao = models.DateTimeField(
        blank=True, null=True, verbose_name='Data da devolucao'
    )
    data_limite = models.DateTimeField(verbose_name='Data limite')
    status = models.CharField(
        max_length=15,
        default='ativo',
        choices=STATUS_CHOICES,
        verbose_name='Status',
    )
    renovacoes = models.IntegerField(default=0, verbose_name='Numero de renovacoes')

    class Meta:
        db_table = 'emprestimo'
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = ['-data_emprestimo']

    def __str__(self):
        return f"Emprestimo #{self.id} - {self.id_leitor.nome} -> {self.id_livro.titulo}"
