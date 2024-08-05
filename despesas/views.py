from django.shortcuts import render
from django.views import View
from .models import Categoria, Despesa
# Create your views here.
class GerenciarCArtegoriaView(View): 
    template_name= "despesas/gerenciar_categoria.html"
    def get(self, request):
        categorias= Categoria.objects.filter(usuario=request.user)
        context = { 
            'categorias',categorias
        }
        return render(request,self.template_name, context)