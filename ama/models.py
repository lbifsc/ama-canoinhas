from django.db import models
from django.utils import timezone


class Noticia(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    capa = models.ImageField(upload_to='noticias/')
    texto = models.TextField()
    data_publicacao = models.DateField(
        default=timezone.now, blank=True, null=True, verbose_name='Data de publicação')

    def __str__(self):
        return self.titulo


class Parceiro(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='parceiros/')

    def __str__(self):
        return self.nome
