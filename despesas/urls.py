from django.urls import path
from .views import GerenciarCategoriaView,EditarCategoriaView,ExcluirCategoriaView, EditarDepositoView,ExcluirDepositoView,ListaDespesasView,AdicionarDespesaView,ExcluirDespesaView,EditarDespesaView,EstatisticaView,AdicionarDepositoView,ListaDepositosView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('categorias/',view=GerenciarCategoriaView.as_view(),name='gerenciar_categorias'),
    path('categorias/editar/<int:pk>/', EditarCategoriaView.as_view(), name='editar_categoria'),
    path('categorias/excluir/<int:pk>/', ExcluirCategoriaView.as_view(), name='excluir_categoria'),
    path('despesas/',view=ListaDespesasView.as_view(),name='lista_despesas'),
    path('despesas/adicionar/',view=AdicionarDespesaView.as_view(),name='adicionar_despesas'),
    path('despesas/excluir/<int:pk>/',view=ExcluirDespesaView.as_view(),name='excluir_despesa'),
    path('despesas/editar/<int:pk>/', view=EditarDespesaView.as_view(),name='editar_despesa'),
    path('',view=EstatisticaView.as_view(),name='estatisticas'),
    path('login/', auth_views.LoginView.as_view(template_name='despesas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registrar/', views.registrar_view, name='registrar'),
    path('adicionar-deposito/', AdicionarDepositoView.as_view(), name='adicionar_deposito'),
    path('lista-depositos/', ListaDepositosView.as_view(), name='lista_depositos'),
    path('despositos/editar/<int:pk>/', EditarDepositoView.as_view(), name='editar_deposito'),
    path('depositos/excluir/<int:pk>/', ExcluirDepositoView.as_view(), name='excluir_deposito'),


]