from django.urls import path
from . import views

app_name = 'loja'


urlpatterns = [
    # Loja
    path('loja/', view=views.LojaGeral.as_view(), name='loja_geral'),
    path('loja/<int:pk>', view=views.LojaItem.as_view(), name='loja_item'),

    # Produto
    path('add_produto/', views.AdicionarProduto.as_view(), name='add_produto'),
    path('editar_produto/<int:pk>', views.EditarProduto.as_view(), name='editar_produto'),
    path('excluir_produto/<int:pk>', views.excluir_produto, name='excluir_produto'),
    path('dashboard/produtos/', view=views.DashboardProdutos.as_view(), name='dashboard_produtos'),

    # Categoria
    path('add_categoria/', views.AdicionarCategoria.as_view(), name='add_categoria'),
    path('editar_categoria/<int:pk>', views.EditarCategoria.as_view(), name='editar_categoria'),
    path('excluir_categoria/<int:pk>', views.excluir_categoria, name='excluir_categoria'),
    path('dashboard/categorias/', view=views.DashboardCategorias.as_view(), name='dashboard_categorias'),
]
