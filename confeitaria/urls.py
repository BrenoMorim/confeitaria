from django.urls import path
from confeitaria.views import index, busca, detalhes_doce

urlpatterns = [
    path('', index, name='index'),
    path('busca', busca, name='busca'),
    path('produtos/<int:doce_id>', detalhes_doce, name='produtos')
]