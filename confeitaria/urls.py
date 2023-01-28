from django.urls import path
from confeitaria.views import index

urlpatterns = [
    path('', index, name='index'),
]