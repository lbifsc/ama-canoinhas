from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import render


class Index(View):
    def get(self, *args, **kwargs):
        return HttpResponse('<h1>Olá mundo</h1>')
