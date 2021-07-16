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


class Mensagem(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=200)
    telefone = models.CharField(max_length=20)
    assunto = models.CharField(max_length=150)
    mensagem = models.TextField()
    data = models.DateField(default=timezone.now)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
