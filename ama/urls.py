from . import views
from django.urls import path


app_name = 'ama'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sobre/', views.Sobre.as_view(), name='sobre'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('doacao/', views.Doacao.as_view(), name='doacao'),

    # Mensagem
    path('contato/', views.Mensagem.as_view(), name='contato'),
    path('dashboard/mensagens/', views.ListarMensagens.as_view(), name='mensagens'),
    path('detalhes_mensagem/<int:pk>', views.DetalhesMensagem.as_view(), name='detalhes_mensagem'),
    path('excluir_mensagem/<int:pk>', views.excluir_mensagem, name='excluir_mensagem'),
    path('marcar_lida/<int:pk>', views.marcar_lida, name='marcar_lida'),

    # Noticia
    path('escrever_noticia/', views.EscreverNoticia.as_view(), name='escrever_noticia'),
    path('editar_noticia/<slug>', views.EditarNoticia.as_view(), name='editar_noticia'),
    path('excluir_noticia/<int:pk>', views.excluir_noticia, name='excluir_noticia'),
    path('detalhes_noticia/<slug>', views.DetalhesNoticia.as_view(), name='detalhes_noticia'),
    path('listar_noticias/', view=views.ListarNoticias.as_view(), name='listar_noticias'),
    path('dashboard/noticias/', view=views.DashboardNoticias.as_view(), name='dashboard_noticias'),

    # Parceiro
    path('adicionar_parceiro/', views.AdicionarParceiro.as_view(), name='adicionar_parceiro'),
    path('editar_parceiro/<int:pk>', views.EditarParceiro.as_view(), name='editar_parceiro'),
    path('excluir_parceiro/<int:pk>', views.excluir_parceiro, name='excluir_parceiro'),
    path('dashboard/parceiros/', views.ListarParceiros.as_view(), name='parceiros'),

    # Sobre
    path('sobre/', views.Sobre.as_view(), name='sobre'), 

    # Projeto
    path('escrever_projeto/', views.EscreverProjeto.as_view(), name='escrever_projeto'),
    path('editar_projeto/<slug>', views.EditarProjeto.as_view(), name='editar_projeto'),
    path('excluir_projeto/<int:pk>', views.excluir_projeto, name='excluir_projeto'),
    path('detalhes_projeto/<slug>', views.DetalhesProjeto.as_view(), name='detalhes_projeto'),
    path('listar_projetos/', view=views.ListarProjetos.as_view(), name='listar_projetos'),
    path('dashboard/projetos/', view=views.DashboardProjetos.as_view(), name='dashboard_projetos'),

    # Eventos
    path('escrever_evento/', views.EscreverEvento.as_view(), name='escrever_evento'),
    path('editar_evento/<slug>', views.EditarEvento.as_view(), name='editar_evento'),
    path('excluir_evento/<int:pk>', views.excluir_evento, name='excluir_evento'),
    path('detalhes_evento/<slug>', views.DetalhesEvento.as_view(), name='detalhes_evento'),
    path('listar_evento/', view=views.ListarEventos.as_view(), name='listar_eventos'),
    path('dashboard/eventos/', view=views.DashboardEventos.as_view(), name='dashboard_eventos'),

    # Indicações
    path('escrever_indicacao/', views.EscreverIndicacao.as_view(), name='escrever_indicacao'),
    path('editar_indicacao/<slug>', views.EditarIndicacao.as_view(), name='editar_indicacao'),
    path('excluir_indicacao/<int:pk>', views.excluir_indicacao, name='excluir_indicacao'),
    path('detalhes_indicacao/<slug>', views.DetalhesIndicacao.as_view(), name='detalhes_indicacao'),
    path('listar_indicacoes/', view=views.ListarIndicacoes.as_view(), name='listar_indicacoes'),
    path('dashboard/indicacoes/', view=views.DashboardIndicacoes.as_view(), name='dashboard_indicacoes'),


]
