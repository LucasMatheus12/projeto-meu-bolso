from django.shortcuts import render
from django.views import View
from .models import Categoria, Despesa
# Create your views here.
class ListaDespesas(View):
    template_name='despesas/lista_despesas.html'
    def get(self,request):
        despesas = Despesa.object.filter(usuario = request.user)
        return render(request,self.template_name,{'despesas':despesas})
class GerenciarCategoriaView(View):
    template_name= 'despesas/gerenciar_categorias.html'
    def get(self,request):
        categorias = Categoria.objects.filter(usuario=request.user)
        context = {
            'categorias': categorias,
        }
        return render(request,self.template_name,context)