from django.urls import path
from confeitaria.views import index, busca

urlpatterns = [
    path('', index, name='index'),
    path('busca', busca, name='busca')
]