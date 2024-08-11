from django.urls import path
from .views import GerenciarCategoriaView,ListaDespesa

urlpatterns=[
    path('categorias/',view=GerenciarCategoriaView.as_view(),name='gerenciar_categorias'),
]