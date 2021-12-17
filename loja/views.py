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


class LojaGeral(View):
    template_name = 'loja/loja_geral.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'produtos': models.Produto.objects.all(),
        }

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class LojaItem(View):
    model = models.Produto
    template_name = 'loja/loja_item.html'

    def get(self, *args, **kwargs):
        context = {
            'produto': get_object_or_404(models.Produto, pk=self.kwargs.get('pk'))
        }
        return render(self.request, self.template_name, context)



# Categorias

class AdicionarCategoria(LoginRequiredMixin, View):
    template_name = 'loja/add_categoria.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'addcategoria_form': forms.CategoriaForm(self.request.POST or None, self.request.FILES or None)
        }

        self.addcategoria_form = contexto['addcategoria_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.addcategoria_form.is_valid():
            return self.renderizar

        self.addcategoria_form.save()

        messages.success(
            self.request,
            'Categoria criada com sucesso!', 
        )

        return redirect('loja:dashboard_categorias')


class EditarCategoria(LoginRequiredMixin, View):
    template_name = 'loja/add_categoria.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.categoria = get_object_or_404(models.Categoria, pk=self.kwargs.get('pk'))
        contexto = {
            'addcategoria_form': forms.CategoriaForm(
                self.request.POST or None,
                instance=self.categoria,
            ),
        }

        self.addcategoria_form = contexto['addcategoria_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.addcategoria_form.is_valid():
            return self.renderizar

        self.categoria.nome = self.addcategoria_form['nome'].value()
        self.categoria.save()

        messages.success(
            self.request,
            'Categoria criada com sucesso!', 
        )

        return redirect('loja:dashboard_categorias')


@login_required
def excluir_categoria(request, pk):
    if request.is_ajax():
        if request.POST:
            categoria = get_object_or_404(models.Categoria, pk=pk)
            categoria.delete()

            return JsonResponse('success', safe=False)


class DashboardCategorias(LoginRequiredMixin, ListView):
    model = models.Categoria
    template_name = 'loja/categorias_dashboard.html'
    paginate_by = 15
    filterset_class = filters.CategoriaFilterSet
    ordering = ['nome', ]


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        return context


# Produtos

class AdicionarProduto(LoginRequiredMixin, View):
    template_name = 'loja/add_produto.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        contexto = {
            'addproduto_form': forms.ProdutoForm(self.request.POST or None, self.request.FILES or None)
        }

        self.addproduto_form = contexto['addproduto_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.addproduto_form.is_valid():
            return self.renderizar

        self.addproduto_form.save()

        messages.success(
            self.request,
            'Produto adicionado com sucesso!', 
        )

        return redirect('loja:dashboard_produtos')


class EditarProduto(LoginRequiredMixin, View):
    template_name = 'loja/add_produto.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.produto = get_object_or_404(models.Produto, pk=self.kwargs.get('pk'))
        contexto = {
            'addproduto_form': forms.ProdutoForm(
                self.request.POST or None,
                instance=self.produto,
            ),
        }

        self.addproduto_form = contexto['addproduto_form']

        self.renderizar = render(self.request, self.template_name, contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.addproduto_form.is_valid():
            return self.renderizar

        self.produto.nome = self.addproduto_form['nome'].value()
        self.produto.Categoria = self.addproduto_form['categoria'].value()
        self.produto.quantidade = self.addproduto_form['quantidade'].value()
        self.produto.preco = self.addproduto_form['preco'].value()
        self.produto.preco_promocional = self.addproduto_form['preco_promocional'].value()
        self.produto.descricao = self.addproduto_form['descricao'].value()
        self.produto.save()

        return redirect('loja:dashboard_produtos')


@login_required
def excluir_produto(request, pk):
    if request.is_ajax():
        if request.POST:
            produto = get_object_or_404(models.Produto, pk=pk)
            produto.delete()

            return JsonResponse('success', safe=False)


class DashboardProdutos(LoginRequiredMixin, ListView):
    model = models.Produto
    template_name = 'loja/produtos_dashboard.html'
    paginate_by = 15
    filterset_class = filters.ProdutoFilterSet
    ordering = ['nome', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        return context