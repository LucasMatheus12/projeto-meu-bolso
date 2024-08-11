from django.urls import path
from .views import GerenciarCategoriaView,ListaDespesasView


urlpatterns=[
    path('categorias/',view=GerenciarCategoriaView.as_view(),name='gerenciar_categorias'),
    path('despesas/',view=ListaDespesasView.as_view(),name='lista_despesas'),
]