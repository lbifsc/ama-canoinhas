from django.db import models
from django.core.validators import MinLengthValidator


class Produto(models.Model):
    nome = models.CharField(max_length= 255)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(
        decimal_places=2, 
        max_digits=5, 
        validators=[MinLengthValidator(0.01)],
    )
    preco_promocional = models.FloatField(blank=True, null=True)
    descricao = models.TextField()


class ProdutoFoto(models.Model):
    foto = models.ImageField(upload_to='produto/')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    