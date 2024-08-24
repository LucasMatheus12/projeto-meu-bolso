from django.shortcuts import render
from django.views import View
from .models import Categoria, Despesa
from .forms import CategoriaForm, DespesaForm
from django.shortcuts import render,redirect
from django.db.models import Sum

class EstatisticasView(View):
    template_name='despesa/estatisticas.html'
    def get(self,request):
        estatisticas = Despesa.objects.filter(usuario=request.user).values('categoria_nome').annotate(total=Sum('valor'))

class EditarDespesaView(View):
    template_name = 'despesas/editar_despesa.html'
    def get(self,request,pk):
        despesa = Despesa.objects.get(pk=pk)
        form = DespesaForm(request.user, instance=despesa)
        categoria = Categoria.objects.filter(usuario=request.user)
        return render (request,self.template_name,{'form':form,'despesa':despesa})
    def post(self,request,pk):
        despesa = Despesa.objects.get(pk=pk)
        form = DespesaForm(request.user,request.POST, instance = despesa)
        if form.is_valid():
            form.save()
        categorias = Categoria.objects.filter(usuario = request.user)
        return render (request,self.template_name,{'form':form,'categorias':categorias})
class ExcluirDespesaView(View):
    template_name='despesas/excluir_despesa.html'
    def get(self,request,pk):
        despesa =   Despesa.objects.get(pk=pk)
        return render (request,self.template_name,{'despesa':despesa})
    def post(self,request,pk):
        despesa =   Despesa.objects.get(pk=pk)
        despesa.delete()
        return redirect('lista_despesas')

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