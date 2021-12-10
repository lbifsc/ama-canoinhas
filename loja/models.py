from django.db import models
from django.core.validators import MinLengthValidator


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length= 255)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(
        decimal_places=2, 
        max_digits=5,
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    preco_promocional = models.FloatField(blank=True, null=True)
    descricao = models.TextField()


class ProdutoFoto(models.Model):
    foto = models.ImageField(upload_to='produto/')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    