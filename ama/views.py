from django.http.response import HttpResponse
from django.views import View
from django.shortcuts import render


class Index(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'ama/index.html')
