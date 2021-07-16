from . import models
from django.contrib import admin


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'titulo', 'data_publicacao')
    list_display_links = ('pk', 'titulo', 'data_publicacao')


admin.site.register(models.Noticia, NoticiaAdmin)


class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')


admin.site.register(models.Parceiro, ParceiroAdmin)
