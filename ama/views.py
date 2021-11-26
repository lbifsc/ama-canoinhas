
import os
from . import forms
from . import models
from . import filters
from django.views import View
from django.db.models import query
from django.contrib import messages
from django.http.response import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from .filters import NoticiaFilterSet, MensagemFilterSet, ParceiroFilterSet, ProjetoFilterSet, EventoFilterSet, IndicacaoFilterSet


class Index(View):
    template_name = 'ama/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'ultimos_projetos': models.Projeto.objects.filter(publicado=True).order_by('-data_publicacao')[:2],
            'ultimos_eventos': models.Evento.objects.filter(publicado=True).order_by('-data_publicacao')[:2],
            'ultimas_noticias': models.Noticia.objects.filter(publicado=True).order_by('-data_publicacao')[:5],
            'ultimas_indicacoes' : models.Indicacao.objects.filter(publicado=True).order_by('-data_publicacao')[:4],
            'parceiros': models.Parceiro.objects.all(),
        }

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

class EscreverNoticia(LoginRequiredMixin, View):
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

        messages.success = (self.request, 'Notícia salva com sucesso!')

        return redirect('ama:detalhes_noticia', slug=noticia.slug)


class EditarNoticia(LoginRequiredMixin, View):
    template_name = 'ama/escrever_noticia.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.noticia = get_object_or_404(
            models.Noticia, slug=self.kwargs.get('slug'))
        self.capa_atual_path = self.noticia.capa.path

        contexto = {
            'noticia_form': forms.NoticiaForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.noticia,
            ),
        }

        self.noticia_form = contexto['noticia_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.noticia_form.is_valid():
            return self.renderizar

        self.noticia.titulo = self.noticia_form['titulo'].value()
        self.noticia.publicado = self.noticia_form['publicado'].value()
        self.noticia.texto = self.noticia_form['texto'].value()

        if self.request.FILES.get('capa'):
            self.noticia.capa = self.request.FILES.get('capa')
            os.remove(self.capa_atual_path)

        self.noticia.save()

        return redirect('ama:detalhes_noticia', slug=self.noticia.slug)


@login_required
def excluir_noticia(request, pk):
    if request.is_ajax():
        if request.POST:
            noticia = get_object_or_404(models.Noticia, pk=pk)
            os.remove(noticia.capa.path)
            noticia.delete()

            return JsonResponse('success', safe=False)


class ListarNoticias(ListView):
    model = models.Noticia
    template_name = 'ama/listar_noticias.html'
    paginate_by = 15
    filterset_class = NoticiaFilterSet

    def get_queryset(self):
        queryset = super().get_queryset().filter(publicado=True).order_by('-data_publicacao')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetalhesNoticia(DetailView):
    model = models.Noticia
    template_name = 'ama/detalhes_noticia.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['noticia'] = get_object_or_404(
                models.Noticia,
                slug=self.kwargs.get('slug'),
            )
        else:
            context['noticia'] = get_object_or_404(
                models.Noticia,
                slug=self.kwargs.get('slug'),
                publicado=True,
            )

        return context


class Sobre(View):
    template_name='ama/sobre.html'

    def get(self, *args, **kwargs):
        return render(self.request, 'ama/sobre.html')


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


class ListarMensagens(LoginRequiredMixin, ListView):
    model = models.Mensagem
    template_name = 'ama/mensagens.html'
    paginate_by = 30
    filterset_class = MensagemFilterSet
    ordering = ['-data', ]

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetalhesMensagem(DetailView):
    template_name = 'ama/detalhes_mensagem.html'
    model = models.Mensagem

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        mensagem = get_object_or_404(models.Mensagem, pk=self.kwargs.get('pk'))
        if not mensagem.lida:
            mensagem.lida = True
            mensagem.save()

        context['mensagem'] = mensagem

        return context


@login_required
def excluir_mensagem(request, pk):
    if request.is_ajax():
        if request.POST:
            get_object_or_404(models.Mensagem, pk=pk).delete()

            return JsonResponse('success', safe=False)


@login_required
def marcar_lida(request, pk):
    if request.is_ajax():
        if request.POST:
            mensagem = get_object_or_404(models.Mensagem, pk=pk)
            lida = request.POST.get('lida')

            if lida == 'true':
                mensagem.lida = True
            else:
                mensagem.lida = False

            mensagem.save()
            response = {
                'success': 'success',
                'lida': mensagem.lida,
            }

            return JsonResponse(response, safe=False)


class AdicionarParceiro(LoginRequiredMixin, View):
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

        messages.success(
            self.request,
            'Parceiro adicionado com sucesso!', 
        )

        return redirect('ama:parceiros')


class ListarParceiros(LoginRequiredMixin, ListView):
    model = models.Parceiro
    template_name = 'ama/parceiros.html'
    paginate_by = 15
    filterset_class = ParceiroFilterSet
    ordering = ['nome', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class EditarParceiro(LoginRequiredMixin, View):
    template_name = 'ama/adicionar_parceiro.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.parceiro = get_object_or_404(
            models.Parceiro, pk=self.kwargs.get('pk'))

        self.logo_atual_path = self.parceiro.logo.path

        contexto = {
            'parceiro_form': forms.ParceiroForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.parceiro,
            )
        }

        self.parceiro_form = contexto['parceiro_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.parceiro_form.is_valid():
            return self.renderizar

        self.parceiro.nome = self.parceiro_form.cleaned_data.get('nome')

        if self.request.FILES.get('logo'):
            self.parceiro.logo = self.request.FILES.get('logo')
            os.remove(self.logo_atual_path)

        self.parceiro.save()

        messages.success(self.request, 'Parceiro editado com sucesso!')

        return redirect('ama:dashboard')


@login_required
def excluir_parceiro(request, pk):
    if request.is_ajax():
        if request.POST:
            parceiro = get_object_or_404(models.Parceiro, pk=pk)
            os.remove(parceiro.logo.path)
            parceiro.delete()

            return JsonResponse('success', safe=False)


class Dashboard(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return redirect('ama:mensagens')


class Login(View):
    template_name = 'ama/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        user = authenticate(
            username=self.request.POST.get('username'),
            password=self.request.POST.get('password'),
        )

        if not user:
            messages.error(self.request, 'Nome de usuário ou senha incorretos!')
            return redirect('ama:login')
        else:
            login(self.request, user)

        if self.request.GET.get('next') is None:
            return redirect('ama:dashboard')
        else: 
            return redirect(self.request.GET.get('next'))


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('ama:index')


class Doacao(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'ama/doacao.html')


class EscreverProjeto(LoginRequiredMixin, View):
    template_name = 'ama/escrever_projeto.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'projeto_form': forms.ProjetoForm(self.request.POST or None, self.request.FILES or None)
        }

        self.projeto_form = contexto['projeto_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.projeto_form.is_valid():
            return self.renderizar

        projeto = self.projeto_form.save()

        messages.success = (self.request, 'Projeto salvo com sucesso!')

        return redirect('ama:detalhes_projeto', slug=projeto.slug)


class EditarProjeto(LoginRequiredMixin, View):
    template_name = 'ama/escrever_projeto.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.projeto = get_object_or_404(models.Projeto, slug=self.kwargs.get('slug'))
        self.capa_atual_path = self.projeto.capa.path

        contexto = {
            'projeto_form': forms.ProjetoForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.projeto,
            ),
        }

        self.projeto_form = contexto['projeto_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.projeto_form.is_valid():
            return self.renderizar

        self.projeto.titulo = self.projeto_form['titulo'].value()
        self.projeto.publicado = self.projeto_form['publicado'].value()
        self.projeto.texto = self.projeto_form['texto'].value()

        if self.request.FILES.get('capa'):
            self.projeto.capa = self.request.FILES.get('capa')
            os.remove(self.capa_atual_path)

        self.projeto.save()

        return redirect('ama:detalhes_projeto', slug=self.projeto.slug)


@login_required
def excluir_projeto(request, pk):
    if request.is_ajax():
        if request.POST:
            projeto = get_object_or_404(models.Projeto, pk=pk)
            os.remove(projeto.capa.path)
            projeto.delete()

            return JsonResponse('success', safe=False)


class ListarProjetos(ListView):
    model = models.Projeto
    template_name = 'ama/listar_projetos.html'
    paginate_by = 15
    filterset_class = ProjetoFilterSet

    def get_queryset(self):
        queryset = super().get_queryset().filter(publicado=True).order_by('-data_publicacao')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetalhesProjeto(DetailView):
    model = models.Projeto
    template_name = 'ama/detalhes_projeto.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['projeto'] = get_object_or_404(
                models.Projeto,
                slug=self.kwargs.get('slug'),
            )
        else:
            context['projeto'] = get_object_or_404(
                models.Projeto,
                slug=self.kwargs.get('slug'),
                publicado=True,
            )

        return context



class EscreverEvento(LoginRequiredMixin, View):
    template_name = 'ama/escrever_evento.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'evento_form': forms.EventoForm(self.request.POST or None, self.request.FILES or None)
        }

        self.evento_form = contexto['evento_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.evento_form.is_valid():
            return self.renderizar

        evento = self.evento_form.save()

        messages.success = (self.request, 'Evento salvo com sucesso!')

        return redirect('ama:detalhes_evento', slug=evento.slug)


class EditarEvento(LoginRequiredMixin, View):
    template_name = 'ama/escrever_evento.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.evento = get_object_or_404(
            models.Evento, slug=self.kwargs.get('slug'))
        self.capa_atual_path = self.evento.capa.path

        contexto = {
            'evento_form': forms.EventoForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.evento,
            ),
        }

        self.evento_form = contexto['evento_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.evento_form.is_valid():
            return self.renderizar

        self.evento.titulo = self.evento_form['titulo'].value()
        self.evento.publicado = self.evento_form['publicado'].value()
        self.evento.texto = self.evento_form['texto'].value()

        if self.request.FILES.get('capa'):
            self.evento.capa = self.request.FILES.get('capa')
            os.remove(self.capa_atual_path)

        self.evento.save()

        return redirect('ama:detalhes_evento', slug=self.evento.slug)


@login_required
def excluir_evento(request, pk):
    if request.is_ajax():
        if request.POST:
            evento = get_object_or_404(models.Evento, pk=pk)
            os.remove(evento.capa.path)
            evento.delete()

            return JsonResponse('success', safe=False)


class ListarEventos(ListView):
    model = models.Evento
    template_name = 'ama/listar_eventos.html'
    paginate_by = 15
    filterset_class = EventoFilterSet

    def get_queryset(self):
        queryset = super().get_queryset().filter(publicado=True).order_by('-data_publicacao')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetalhesEvento(DetailView):
    model = models.Evento
    template_name = 'ama/detalhes_evento.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['evento'] = get_object_or_404(
                models.Evento,
                slug=self.kwargs.get('slug'),
            )
        else:
            context['evento'] = get_object_or_404(
                models.Evento,
                slug=self.kwargs.get('slug'),
                publicado=True,
            )

        return context


class EscreverIndicacao(LoginRequiredMixin, View):
    template_name = 'ama/escrever_indicacao.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'indicacao_form': forms.IndicacaoForm(self.request.POST or None, self.request.FILES or None)
        }

        self.indicacao_form = contexto['indicacao_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.indicacao_form.is_valid():
            return self.renderizar

        indicacao = self.indicacao_form.save()

        messages.success = (self.request, 'Indicação salva com sucesso!')

        return redirect('ama:detalhes_indicacao', slug=indicacao.slug)


class EditarIndicacao(LoginRequiredMixin, View):
    template_name = 'ama/escrever_indicacao.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.indicacao = get_object_or_404(
            models.Indicacao, slug=self.kwargs.get('slug'))
        self.capa_atual_path = self.indicacao.capa.path

        contexto = {
            'indicacao_form': forms.IndicacaoForm(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.indicacao,
            ),
        }

        self.indicacao_form = contexto['indicacao_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.indicacao_form.is_valid():
            return self.renderizar

        self.indicacao.titulo = self.indicacao_form['titulo'].value()
        self.indicacao.publicado = self.indicacao_form['publicado'].value()
        self.indicacao.texto = self.indicacao_form['texto'].value()

        if self.request.FILES.get('capa'):
            self.indicacao.capa = self.request.FILES.get('capa')
            os.remove(self.capa_atual_path)

        self.indicacao.save()

        return redirect('ama:detalhes_indicacao', slug=self.indicacao.slug)


@login_required
def excluir_indicacao(request, pk):
    if request.is_ajax():
        if request.POST:
            indicacao = get_object_or_404(models.Indicacao, pk=pk)
            os.remove(indicacao.capa.path)
            indicacao.delete()

            return JsonResponse('success', safe=False)


class ListarIndicacoes(ListView):
    model = models.Indicacao
    template_name = 'ama/listar_indicacoes.html'
    paginate_by = 15
    filterset_class = IndicacaoFilterSet

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_publicacao')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetalhesIndicacao(DetailView):
    model = models.Indicacao
    template_name = 'ama/detalhes_indicacao.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['indicacao'] = get_object_or_404(
                models.Indicacao,
                slug=self.kwargs.get('slug'),
            )
        else:
            context['indicacao'] = get_object_or_404(
                models.Indicacao,
                slug=self.kwargs.get('slug'),
                publicado=True,
            )

        return context


# DashboardViews
class DashboardNoticias(LoginRequiredMixin, ListView):
    model = models.Noticia
    template_name = 'ama/noticias_dashboard.html'
    paginate_by = 15
    filterset_class = filters.DashboardFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, placeholder='Buscar Notícias')
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        return context

    
class DashboardProjetos(LoginRequiredMixin, ListView):
    model = models.Projeto
    template_name = 'ama/projetos_dashboard.html'
    paginate_by = 15
    filterset_class = filters.DashboardFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, placeholder='Buscar Projetos')
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context 


class DashboardEventos(LoginRequiredMixin, ListView):
    model = models.Evento
    template_name = 'ama/eventos_dashboard.html'
    paginate_by = 15
    filterset_class = filters.DashboardFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, placeholder='Buscar Eventos')
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        return context

class DashboardIndicacoes(LoginRequiredMixin, ListView):
    model = models.Indicacao
    template_name = 'ama/indicacoes_dashboard.html'
    paginate_by = 15
    filterset_class = filters.DashboardFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, placeholder='Buscar Indicações')
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        return context