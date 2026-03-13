"""
Model: Emprestimo (Loan)
Componente responsavel pelo gerenciamento dos emprestimos da biblioteca.
"""

from django.db import models


class Emprestimo(models.Model):
    """Modelo de dados do Emprestimo."""

    id_leitor = models.ForeignKey(
        "leitor.Leitor",
        on_delete=models.CASCADE,
        related_name="emprestimos",
        verbose_name="Leitor",
    )
    id_livro = models.ForeignKey(
        "livro.Livro",
        on_delete=models.CASCADE,
        related_name="emprestimos",
        verbose_name="Livro",
    )
    data_emprestimo = models.DateTimeField(
        auto_now_add=True, verbose_name="Data do emprestimo"
    )
    data_devolucao = models.DateTimeField(
        blank=True, null=True, verbose_name="Data da devolucao"
    )
    data_limite = models.DateTimeField(verbose_name="Data limite para devolucao")
    status = models.CharField(
        max_length=15, default="ativo", verbose_name="Status"
    )

    class Meta:
        db_table = "emprestimo"
        verbose_name = "Emprestimo"
        verbose_name_plural = "Emprestimos"

    def __str__(self):
        return f"Emprestimo #{self.id} - {self.id_leitor} -> {self.id_livro}"
