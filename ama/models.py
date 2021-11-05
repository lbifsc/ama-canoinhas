from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Noticia(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    capa = models.ImageField(upload_to='noticias/')
    texto = models.TextField()
    publicado = models.BooleanField(default=False)
    data_publicacao = models.DateTimeField(
        blank=True, null=True, verbose_name='Data de publicação')
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        super().save()

        if not self.slug:
            self.slug = f'{slugify(self.titulo)}-{str(self.pk)}'

        if not self.data_publicacao:
            if self.publicado:
                self.data_publicacao = timezone.now()
            else:
                self.data_publicacao = None

        super().save(*args, **kwargs)

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

class Projeto(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    capa = models.ImageField(upload_to='projetos/')
    texto = models.TextField()
    publicado = models.BooleanField(default=False)
    data_publicacao = models.DateTimeField(
        blank=True, null=True, verbose_name='Data de publicação')
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        super().save()

        if not self.slug:
            self.slug = f'{slugify(self.titulo)}-{str(self.pk)}'

        if not self.data_publicacao:
            if self.publicado:
                self.data_publicacao = timezone.now()
            else:
                self.data_publicacao = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Evento(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    capa = models.ImageField(upload_to='eventos/')
    texto = models.TextField()
    publicado = models.BooleanField(default=False)
    data_publicacao = models.DateTimeField(blank=True, null=True, verbose_name='Data de publicação')
    data_evento = models.DateField(blank=True, null=True, verbose_name='Data do evento')
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        super().save()

        if not self.slug:
            self.slug = f'{slugify(self.titulo)}-{str(self.pk)}'

        if not self.data_publicacao:
            if self.publicado:
                self.data_publicacao = timezone.now()
            else:
                self.data_publicacao = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Indicacao(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    capa = models.ImageField(upload_to='indicacao/')
    texto = models.TextField()
    publicado = models.BooleanField(default=False)
    data_publicacao = models.DateTimeField(
        blank=True, null=True, verbose_name='Data de publicação')
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        super().save()

        if not self.slug:
            self.slug = f'{slugify(self.titulo)}-{str(self.pk)}'

        if not self.data_publicacao:
            if self.publicado:
                self.data_publicacao = timezone.now()
            else:
                self.data_publicacao = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
