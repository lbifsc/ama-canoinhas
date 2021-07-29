from . import models
from django_filters import FilterSet
from django.db.models.query_utils import Q 
from django_filters.filters import CharFilter, ChoiceFilter


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
        return queryset.filter(titulo__icontains=value)


class MensagemFilterSet(FilterSet):
    select_order = ChoiceFilter(
        choices={
            ('-data', 'Mais recentes'),
            ('data', 'Mais antigas'),
            ('lida', 'Não lidas'),
            ('-lida', 'Lidas'),
        },
        method = 'filter_select_order',
    )

    search = CharFilter(method='search_filter')

    class Meta:
        model = models.Mensagem
        fields = {}

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data', '-data')
        super().__init__(data, *args, **kwargs)

        self.filters['select_order'].field.widget.attrs.update({'class': 'form-control col-lg-12'})
        self.filters['search'].field.widget.attrs.update({
            'class': 'form-control col-lg-12',
            'placeholder': 'Buscar mensagem',
            'style': 'height: 100%;',
        })

    def filter_select_order(self, queryset, name, value):
        return queryset.order_by(value)

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(assunto__icontains=value) |
            Q(nome__icontains=value) | 
            Q(mensagem__icontains=value)
        )