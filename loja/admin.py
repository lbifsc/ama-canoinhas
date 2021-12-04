from . import models
from django.contrib import admin


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome')
    list_display_links = ('pk', 'nome')


admin.site.register(models.Categoria, CategoriaAdmin)


class ProdutoFotoInline(admin.TabularInline):
    model = models.ProdutoFoto
    extra = 0


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'quantidade', 'preco', 'preco_promocional', 'categoria')
    list_display_links = ('pk', 'nome', 'quantidade', 'preco', 'preco_promocional', 'categoria')

    inlines = [ProdutoFotoInline]

admin.site.register(models.Produto, ProdutoAdmin)
