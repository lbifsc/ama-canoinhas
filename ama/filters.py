from os import name
from django_filters import FilterSet
from django_filters.filters import CharFilter, ChoiceFilter
from . import models


class NoticiaFilterSet(FilterSet):
    data_publicacao = ChoiceFilter(
        label='Filtrar por:',
        choices=(
            ('-data_publicacao','Mais recentes'),
            ('data_publicacao','Mais antigas'),
        ),
        method='filter_data_publicacao',
    )

    titulo = CharFilter(
        method='filter_titulo'
    )

    class Meta:
        model = models.Noticia
        fields = {}
    
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data_publicacao', '-data_publicacao')
        super().__init__(data, *args, **kwargs)

        self.filters['data_publicacao'].field.widget.attrs.update({'class': 'form-control col-lg-12'})
        self.filters['titulo'].field.widget.attrs.update({'class': 'form-control col-lg-12', 'style': 'height: 100%;', 'placeholder': 'Buscar notícia'})

    def filter_data_publicacao(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_titulo(self, queryset, name, value):
        print(value)
        return queryset.filter(titulo__contains__=value)
