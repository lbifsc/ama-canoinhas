from . import models
from django.contrib import admin


class ProdutoFotoInline(admin.TabularInline):
    model = models.ProdutoFoto
    extra = 0


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'quantidade', 'preco')
    list_display_links = ('pk', 'nome', 'quantidade', 'preco')

    inlines = [ProdutoFotoInline]

admin.site.register(models.Produto, ProdutoAdmin)
