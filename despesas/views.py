from django.shortcuts import render
from django.views import View
from .models import Categoria, Despesa
# Create your views here.
class GerenciarCategoriaView(View):
    template_name= 'despesas/gerenciar_categorias.html'
    def get(self,request):
        categorias = Categoria.objects.filter(usuario=request.user)
        context = {
            'categorias': categorias,
        }
        return render(request,self.template_name,context)