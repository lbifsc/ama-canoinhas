from . import forms
from . import models
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView
from django.shortcuts import redirect, render
from django.http.response import HttpResponse


class Index(View):
    template_name = 'ama/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'ultimas_noticias': models.Noticia.objects.filter(publicado=True).order_by('data_publicacao')[:5]
        }

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class EscreverNoticia(View):
    template_name = 'ama/escrever_noticia.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'noticia_form': forms.NoticiaForm(self.request.POST or None, self.request.FILES or None)
        }

        self.noticia_form = contexto['noticia_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.noticia_form.is_valid():
            return self.renderizar

        self.noticia_form.save()
        print('\n{}\n'.format(self.noticia_form.cleaned_data.get('titulo')))

        messages.success = (self.request, 'Notícia salva com sucesso!')

        return HttpResponse('Notícia')


class DetalhesNoticia(DetailView):
    pass


class Sobre(View):
    pass


class Mensagem(View):
    template_name = 'ama/contato.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'mensagem-form': forms.MensagemForm(data=self.request.POST or None),
        }

        self.form = contexto['mensagem-form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.form.is_valid():
            return self.renderizar

        self.form.save()

        messages.success(
            self.request,
            'Mensagem enviada com sucesso!',
        )

        return redirect('ama:contato')
