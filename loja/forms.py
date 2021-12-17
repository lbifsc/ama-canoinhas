from . import models
from django import forms
from django.utils import timezone
from .models import Produto, Categoria
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Row, Column, Submit

class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(max_length=150, required=True, label='Nome:',)
    categoria = forms.ModelChoiceField(Categoria.objects.all())
    quantidade = forms.IntegerField()
    preco = forms.DecimalField(
        decimal_places=2, 
        max_digits=5,
    )
    preco_promocional = forms.DecimalField(
        decimal_places=2, 
        max_digits=5, 
    )
    descricao = forms.CharField(max_length=150, required=True, label='descricao:',)

    class Meta:
        model = models.Produto
        fields = ['nome', 'categoria', 'quantidade', 'preco', 'preco_promocional', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.method = 'POST'

        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-lg-12'),
            ),
            Row(
                Column('categoria', css_class='col-lg-12'),
            ),
            Row(
                Column('quantidade', css_class='col-lg-12'),
            ),
            Row(
                Column('preco', css_class='col-lg-12'),
            ),
            Row(
                Column('preco_promocional', css_class='col-lg-12'),
            ),
            Row(
                Column('descricao', css_class='col-lg-12'),
            ),
            ButtonHolder(
                Submit('submit', 'Salvar')
            ),
        )

class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(max_length=150, required=True, label='Nome:',)

    class Meta:
        model = models.Categoria
        fields = ['nome', ]

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.method = 'POST'

        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-lg-12'),
            ),
            ButtonHolder(
                Submit('submit', 'Salvar', css_class='mb-3')
            ),
        )