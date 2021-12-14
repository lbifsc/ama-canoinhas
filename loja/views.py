from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin


class LojaGeral(View):
    template_name = 'loja/loja_geral.html'

    def get(self, request):
        return render(request, self.template_name)

class LojaItem(View):
    template_name = 'loja/loja_item.html'

    def get(self,request):
        return render(request, self.template_name)

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

        return redirect('loja:loja_geral')

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

        return redirect('loja:add_produto')