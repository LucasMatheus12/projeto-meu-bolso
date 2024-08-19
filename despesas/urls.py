from django.urls import path
from .views import GerenciarCategoriaView,ListaDespesasView,AdicionarDespesaView,ExcluirDespesaView


urlpatterns=[
    path('categorias/',view=GerenciarCategoriaView.as_view(),name='gerenciar_categorias'),
    path('despesas/',view=ListaDespesasView.as_view(),name='lista_despesas'),
    path('despesas/adicionar/',view=AdicionarDespesaView.as_view(),name='adicionar_despesas'),
    path('despesas/excluir/<int:pk>/',view=ExcluirDespesaView.as_view(),name='excluir_despesa'),
    path('despesas/editar/<int:pk>/', view=EditarDespesaView.as_view(),name='editar_despesa'),
]