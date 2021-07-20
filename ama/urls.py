from . import views
from django.urls import path


app_name = 'ama'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('escrever_noticia/', views.EscreverNoticia.as_view(),
         name='escrever_noticia'),
    path('detalhes_noticia/<slug>', views.DetalhesNoticia.as_view(),
         name='detalhes_noticia'),
    path('listar_noticias/', view=views.ListarNoticias.as_view(),
         name='listar_noticias'),
    path('sobre/', views.Sobre.as_view(), name='sobre'),
    path('contato/', views.Mensagem.as_view(), name='contato'),
    path('adicionar_parceiro/', views.AdicionarParceiro.as_view(),
         name='adicionar_parceiro'),
]
