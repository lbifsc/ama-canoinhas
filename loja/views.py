from django.shortcuts import render
from django.views import View


class LojaGeral(View):
    template_name = 'loja/loja_geral.html'

    def get(self, request):
        return render(request, self.template_name)

class LojaItem(View):
    template_name = 'loja/loja_item.html'

    def get(self,request):
        return render(request, self.template_name)