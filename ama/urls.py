from . import views
from django.urls import path


app_name = 'ama'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('detalhes_noticia', views.DetalhesNoticia.as_view(),
         name='detalhes_noticia'),
    path('sobre/', views.Sobre.as_view(), name='sobre'),
    path('contato/', views.Mensagem.as_view(), name='contato'),
]
