from . import models
from django.contrib import admin


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'titulo', 'data_publicacao', 'publicado', )
    list_display_links = ('pk', 'titulo', 'data_publicacao', )
    list_editable = ('publicado', )


admin.site.register(models.Noticia, NoticiaAdmin)


class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')


admin.site.register(models.Parceiro, ParceiroAdmin)


class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone',
                    'assunto', 'data', 'lida',)
    list_display_links = ('id', 'nome', 'email',
                          'telefone', 'assunto', 'data',)
    list_editable = ('lida', )


admin.site.register(models.Mensagem, MensagemAdmin)
