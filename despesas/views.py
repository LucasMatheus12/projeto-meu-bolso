from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Despesa, Deposito
from .forms import CategoriaForm, DespesaForm, LoginForm, RegistroForm,DepositoForm
import json

def registrar_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Registro concluído com sucesso!")
            return redirect('lista_despesas')  
    else:
        form = RegistroForm()
    return render(request, 'despesas/registrar.html', {'form': form})


@login_required
def pagina_inicial(request):
    return render(request, 'despesas/login.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_despesas')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados e tente novamente.')
    else:
        form = LoginForm()
    
    return render(request, 'despesas/login.html', {'form': form})


class EstatisticaView(View):
    template_name = 'despesas/estatisticas.html'

    def get(self, request):
        estatisticas = Despesa.objects.filter(usuario=request.user).values('categoria__nome').annotate(total=Sum('valor'))
        total_valores = Despesa.objects.filter(usuario=request.user).aggregate(total=Sum('valor'))['total']
        categorias = [estatistica['categoria__nome'] for estatistica in estatisticas]
        valores = [float(estatistica['total']) for estatistica in estatisticas]
        categorias_django = json.dumps(categorias)
        valores_django = json.dumps(valores)
        context = {
            'categorias_django': categorias_django,
            'valores_django': valores_django,
            'total_despesas': total_valores,
        }
        return render(request, self.template_name, context)


class EditarDespesaView(View):
    template_name = 'despesas/editar_despesa.html'

    def get(self, request, pk):
        despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
        form = DespesaForm(request.user, instance=despesa)
        return render(request, self.template_name, {'form': form, 'despesa': despesa})

    def post(self, request, pk):
        despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
        form = DespesaForm(request.user, request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect('lista_despesas')
        messages.error(request, "Erro ao atualizar a despesa.")
        return render(request, self.template_name, {'form': form, 'despesa': despesa})


class ExcluirDespesaView(View):
    template_name = 'despesas/excluir_despesas.html'

    def get(self, request, pk):
        despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
        return render(request, self.template_name, {'despesa': despesa})

    def post(self, request, pk):
        despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
        despesa.delete()
        messages.success(request, "Despesa excluída com sucesso!")
        return redirect('lista_despesas')


from django.contrib import messages

class AdicionarDespesaView(View):
    template_name= 'despesas/adicionar_despesas.html'
    
    def get(self, request):
        categorias = Categoria.objects.filter(usuario=request.user)
        form = DespesaForm(user=request.user)
        context = {
            'categorias': categorias,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = DespesaForm(request.user, request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            messages.success(request, 'Despesa adicionada com sucesso!')
            return redirect('lista_despesas')
        else:
            messages.error(request, 'Erro ao adicionar despesa. Por favor, corrija os erros e tente novamente.')
        
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'categorias': categorias, 'form': form})



class ListaDespesasView(View):
    template_name = 'despesas/lista_despesas.html'

    def get(self, request):
        despesas = Despesa.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'despesas': despesas})


class GerenciarCategoriaView(View):
    template_name = 'despesas/gerenciar_categorias.html'

    def get(self, request):
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'categorias': categorias})

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, "Categoria adicionada com sucesso!")
            return redirect('gerenciar_categorias')
        messages.error(request, "Erro ao adicionar a categoria.")
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'categorias': categorias, 'form': form})

class AdicionarDepositoView(View):
    template_name = 'despesas/adicionar_deposito.html'

    def get(self, request):
        form = DepositoForm(user=request.user)
        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'form': form, 'categorias': categorias})

    def post(self, request):
        form = DepositoForm(request.user, request.POST)
        if form.is_valid():
            deposito = form.save(commit=False)
            deposito.usuario = request.user
            deposito.save()
            messages.success(request, 'Depósito adicionado com sucesso!')
            return redirect('lista_depositos') 
        else:
            messages.error(request, 'Erro ao adicionar depósito. Por favor, corrija os erros e tente novamente.')

        categorias = Categoria.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'form': form, 'categorias': categorias})