from . import models
from django import forms
from .models import Categoria
from crispy_forms.helper import FormHelper
from django_summernote.widgets import SummernoteWidget
from crispy_forms.layout import ButtonHolder, Layout, Row, Column, Submit

class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nome:',
    )
    
    categoria = forms.ModelChoiceField(
        Categoria.objects.all()
    )
    
    quantidade = forms.IntegerField()
    
    preco = forms.DecimalField(
        decimal_places=2, 
        max_digits=5,
        label='Preço',
    )
    preco_promocional = forms.DecimalField(
        decimal_places=2, 
        max_digits=5, 
        label='Preço Promocional:',
    )

    descricao = forms.CharField(
        required=True, 
        label='Descrição:',
        widget=SummernoteWidget(),
    )

    class Meta:
        model = models.Produto
        fields = ['nome', 'categoria', 'quantidade', 'preco', 'preco_promocional', 'descricao', ]

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.method = 'POST'

        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-lg-8'),
                Column('categoria', css_class='col-lg-4'),
            ),
            Row(
                Column('quantidade', css_class='col-lg-4'),
                Column('preco', css_class='col-lg-4'),
                Column('preco_promocional', css_class='col-lg-4'),
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