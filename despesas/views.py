from django.shortcuts import render
from django.views import View
from .models import Categoria, Despesa
from .forms import CategoriaForm, DespesaForm
from django.shortcuts import render,redirect
# Create your views here.

class AdicionarDespesaView(View):
    template_name= 'despesas/adicionar_despesas.html'
    def get(self,request):
        categorias = Categoria.objects.filter(usuario = request.user)
        form = DespesaForm(user=request.user)
        context = {
            'categorias':categorias,
            'form':form,
        }
        return render (request,self.template_name,context)
    def post(self,request):
        form = DespesaForm(request.user,request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            return redirect ('lista_despesas')
        categorias = Categoria.objects.filter(usuario=request.user)
        return render (request, self.template_name,{'categorias':categorias,'form':form})
class ListaDespesasView(View):
    template_name='despesas/lista_despesas.html'
    def get(self,request):
        despesas = Despesa.objects.filter(usuario = request.user)
        return render(request,self.template_name,{'despesas':despesas})
class GerenciarCategoriaView(View):
    template_name= 'despesas/gerenciar_categorias.html'
    def get(self,request):
        categorias = Categoria.objects.filter(usuario=request.user)
        context = {
            'categorias': categorias,
        }
        return render(request,self.template_name,context)
    def post(self,request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            return redirect ('gerenciar_categorias')
        categorias = Categoria.objects.filter(usuario=request.user)
        context = {
            'categorias':categorias,
            'form':form
        }
        return render(request,self.template_name,context)