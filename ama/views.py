from django.core import paginator
from . import forms
from . import models
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render


class Index(View):
    template_name = 'ama/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'ultimas_noticias': models.Noticia.objects.filter(publicado=True).order_by('data_publicacao')[:5],
            'parceiros': models.Parceiro.objects.all(),
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

        noticia = self.noticia_form.save()
        print('\n{}\n'.format(noticia.slug))

        messages.success = (self.request, 'Notícia salva com sucesso!')

        return redirect('ama:detalhes_noticia', slug=noticia.slug)


class ListarNoticias(ListView):
    model = models.Noticia
    template_name = 'ama/listar_noticias.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        noticias = models.Noticia.objects.filter(publicado=True)
        paginator = Paginator(None, self.paginate_by)
        is_paginated = True

        if noticias.count() <= self.paginate_by:
            is_paginated = False

        ordem = self.request.GET.get('ordena-noticias')

        if ordem == 'Mais antigas':
            paginator.object_list = noticias.order_by('data_publicacao')
            context['ordenado'] = True
        else:
            paginator.object_list = noticias.order_by('-data_publicacao')
            context['ordenado'] = False

        context['is_paginated'] = is_paginated
        context['page_obj'] = paginator.get_page(self.request.GET.get('page'))

        return context


class DetalhesNoticia(DetailView):
    model = models.Noticia
    template_name = 'ama/detalhes_noticia.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticia'] = get_object_or_404(
            models.Noticia,
            slug=self.kwargs.get('slug'),
            publicado=True,
        )

        return context


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


class AdicionarParceiro(View):
    template_name = 'ama/adicionar_parceiro.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'parceiro_form': forms.ParceiroForm(self.request.POST or None, self.request.FILES or None)
        }

        self.parceiro_form = contexto['parceiro_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.parceiro_form.is_valid():
            return self.renderizar

        self.parceiro_form.save()

        messages.success(self.request, 'Parceiro adicionado com sucesso!')

        return redirect('ama:adicionar_parceiro')
