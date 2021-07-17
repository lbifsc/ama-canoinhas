from . import forms
from . import models
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView
from django.shortcuts import redirect, render


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
