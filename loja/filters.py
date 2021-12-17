from django.db.models import fields
from . import models
from django_filters import FilterSet
from django.db.models.query_utils import Q 
from django_filters.filters import CharFilter, ChoiceFilter


class CategoriaFilterSet(FilterSet):
    nome = CharFilter(method='nome_filter', )

    class Meta:
        model = models.Categoria
        fields = {}

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data', '-data')
        super().__init__(data, *args, **kwargs)

        self.filters['nome'].field.widget.attrs.update({
            'class': 'form-control col-lg-12', 
            'placeholder': 'Buscar categoria',
            'style': 'height: 100%;',    
        })

    def nome_filter(self, queryset, name, value):
        return queryset.filter(nome__icontains=value)


class ProdutoFilterSet(FilterSet):
    nome = CharFilter(method='nome_filter', )

    class Meta:
        model = models.Produto
        fields = {}

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data', '-data')
        super().__init__(data, *args, **kwargs)

        self.filters['nome'].field.widget.attrs.update({
            'class': 'form-control col-lg-12', 
            'placeholder': 'Buscar produto',
            'style': 'height: 100%;',    
        })

    def nome_filter(self, queryset, name, value):
        return queryset.filter(nome__icontains=value)
