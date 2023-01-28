from django.shortcuts import render
from confeitaria.models import Doce, CATEGORIAS

# Create your views here.

def index(request):

    if not "categoria" in request.GET or request.GET['categoria'] == 'TODOS':
        doces = Doce.objects.all()
    else:
        doces = Doce.objects.filter(categoria=request.GET['categoria'])

    categorias = ["TODOS"] + [categoria[0] for categoria in CATEGORIAS]
    return render(request, "confeitaria/index.html", {
        "doces": doces, 
        "categorias": categorias
    })
