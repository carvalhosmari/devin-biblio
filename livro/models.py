from django.db import models


class Livro(models.Model):
    isbn = models.CharField(max_length=25, verbose_name='ISBN')
    titulo = models.CharField(max_length=200, verbose_name='Titulo')
    autores = models.CharField(max_length=200, verbose_name='Autores')
    pais = models.CharField(max_length=50, blank=True, null=True, verbose_name='Pais')
    editora = models.CharField(max_length=50, blank=True, null=True, verbose_name='Editora')
    edicao = models.CharField(max_length=50, blank=True, null=True, verbose_name='Edicao')
    status = models.CharField(
        max_length=15,
        default='disponivel',
        choices=[
            ('disponivel', 'Disponivel'),
            ('emprestado', 'Emprestado'),
        ],
        verbose_name='Status',
    )

    class Meta:
        db_table = 'livro'
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} (ISBN: {self.isbn}) - ID: {self.id}"
