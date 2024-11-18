from django.shortcuts import render
from django.template import engines
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = "GOODstime/index.html"


    def get(self, request, *args, **kwargs):
        print("Template search paths:", engines['django'].dirs)
        return super().get(request, *args, **kwargs)
