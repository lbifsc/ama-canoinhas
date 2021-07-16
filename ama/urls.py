from . import views
from django.urls import path


app_name = 'ama'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sobre/', views.Sobre.as_view(), name='sobre'),
    path('contato/', views.Mensagem.as_view(), name='contato'),
]
