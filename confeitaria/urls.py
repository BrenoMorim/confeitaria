from django.urls import path
from confeitaria.views import index, busca, detalhes_doce, carrinho, finalizar_pedido

urlpatterns = [
    path('', index, name='index'),
    path('busca', busca, name='busca'),
    path('produtos/<int:doce_id>', detalhes_doce, name='produtos'),
    path('carrinho', carrinho, name='carrinho'),
    path('finalizar', finalizar_pedido, name='finalizar')
]