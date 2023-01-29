from django.shortcuts import render, redirect
from confeitaria.models import Doce, CATEGORIAS

def index(request):

    doces_baratos = Doce.objects.filter(preco__lt=20.0)[:15]

    if not "categoria" in request.GET or request.GET['categoria'] == 'TODOS':
        doces = Doce.objects.all()[:15]
    else:
        doces = Doce.objects.filter(categoria=request.GET['categoria'])[:15]

    categorias = ["TODOS"] + [categoria[0] for categoria in CATEGORIAS]
    return render(request, "confeitaria/index.html", {
        "doces": doces,
        "doces_baratos": doces_baratos,
        "categorias": categorias
    })

def busca(request):
    if request.method != 'POST' or not 'busca' in request.POST:
        return redirect('index')
    
    query = request.POST['busca']
    doces = Doce.objects.filter(nome__contains=query)
    return render(request, 'confeitaria/busca.html', {"doces": doces, "busca": query})