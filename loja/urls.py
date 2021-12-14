from django.urls import path
from . import views

app_name = 'loja'


urlpatterns = [
    # Loja
    path('', view=views.LojaGeral.as_view(), name='loja_geral'),
    path('item/', view=views.LojaItem.as_view(), name='loja_item'),
    path('add_produto/', views.AdicionarProduto.as_view(), name='add_produto'),
    path('add_categoria/', views.AdicionarCategoria.as_view(), name='add_categoria'),
]
