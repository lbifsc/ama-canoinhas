from django.db.models import fields
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
            ('-lida', 'Não lidas'),
            ('lida', 'Lidas'),
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


class ParceiroFilterSet(FilterSet):
    nome = CharFilter(method='nome_filter', )

    class Meta:
        model = models.Parceiro
        fields = {}

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data', '-data')
        super().__init__(data, *args, **kwargs)

        self.filters['nome'].field.widget.attrs.update({
            'class': 'form-control col-lg-12', 
            'placeholder': 'Buscar parceiro',
            'style': 'height: 100%;',    
        })

    def nome_filter(self, queryset, name, value):
        return queryset.filter(nome__icontains=value)


class ProjetoFilterSet(FilterSet):
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
        model = models.Projeto
        fields = {}
    
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data_publicacao', '-data_publicacao')
        super().__init__(data, *args, **kwargs)

        self.filters['data_publicacao'].field.widget.attrs.update({'class': 'form-control col-lg-12'})
        self.filters['titulo'].field.widget.attrs.update({'class': 'form-control col-lg-12', 'style': 'height: 100%;', 'placeholder': 'Buscar projeto'})

    def filter_data_publicacao(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_titulo(self, queryset, name, value):
        return queryset.filter(titulo__icontains=value)


class EventoFilterSet(FilterSet):
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
        model = models.Evento
        fields = {}
    
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data_publicacao', '-data_publicacao')
        super().__init__(data, *args, **kwargs)

        self.filters['data_publicacao'].field.widget.attrs.update({'class': 'form-control col-lg-12'})
        self.filters['titulo'].field.widget.attrs.update({'class': 'form-control col-lg-12', 'style': 'height: 100%;', 'placeholder': 'Buscar evento'})

    def filter_data_publicacao(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_titulo(self, queryset, name, value):
        return queryset.filter(titulo__icontains=value)


class IndicacaoFilterSet(FilterSet):
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
        model = models.Indicacao
        fields = {}
    
    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('data_publicacao', '-data_publicacao')
        super().__init__(data, *args, **kwargs)

        self.filters['data_publicacao'].field.widget.attrs.update({'class': 'form-control col-lg-12'})
        self.filters['titulo'].field.widget.attrs.update({'class': 'form-control col-lg-12', 'style': 'height: 100%;', 'placeholder': 'Buscar Indicacao'})

    def filter_data_publicacao(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_titulo(self, queryset, name, value):
        return queryset.filter(titulo__icontains=value)


# Dashboard Flters
class DashboardFilterSet(FilterSet):

    ordenar = ChoiceFilter(
        method='ordenar_projetos',
        choices=(
            ('-data_publicacao', 'Mais Recentes'),
            ('data_publicacao', 'Mais Antigos'),
            ('-publicado', 'Públicados'),
            ('publicado', 'Não Públicados'),
        ),
    )

    buscar = CharFilter(method='buscar_projeto')

    class Meta:
        model = models.Projeto
        fields = {}

    def __init__(self, data, placeholder, *args, **kwargs):
        data = data.copy()
        super().__init__(data=data, *args, **kwargs) 

        self.placeholder = placeholder

        self.filters['ordenar'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['buscar'].field.widget.attrs.update({'class': 'form-control h-100', 'placeholder': self.placeholder})

    def ordenar_projetos(self, queryset, name, value):
        return queryset.order_by(value)

    def buscar_projeto(self, queryset, name, value):
        return queryset.filter(
            Q(titulo__icontains=value) | 
            Q(texto__icontains=value) 
        )


