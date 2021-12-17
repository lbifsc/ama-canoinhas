from django.db.models import fields
from . import models
from django_filters import FilterSet
from django.db.models.query_utils import Q 
from django_filters.filters import CharFilter, ChoiceFilter


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
        model = models.Produto
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