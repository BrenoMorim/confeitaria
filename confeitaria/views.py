from django.shortcuts import render, redirect
from confeitaria.models import Doce, CATEGORIAS
from django.shortcuts import get_object_or_404

def index(request):

    doces_baratos = Doce.objects.filter(preco__lt=20.0)[:10]
    print(doces_baratos[0].id)
    if not "categoria" in request.GET or request.GET['categoria'] == 'TODOS':
        doces = Doce.objects.all()[:10]
    else:
        doces = Doce.objects.filter(categoria=request.GET['categoria'])[:10]

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
    doces = Doce.objects.filter(nome__icontains=query)
    return render(request, 'confeitaria/busca.html', {"doces": doces, "busca": query})

def detalhes_doce(request, doce_id):
    
    doce = get_object_or_404(Doce, pk=doce_id)
    doces_relacionados = Doce.objects.filter(categoria=doce.categoria)[:10]
    return render(request, 'confeitaria/detalhes.html', 
        {
            "doce": doce,
            "doces_relacionados": [d for d in doces_relacionados if d.id != doce_id]
        }
    )

def carrinho(request):
    if request.method == 'POST':

        if request.POST['tipo'] == 'adicionar':
            if not 'Carrinho' in request.session.keys():
                request.session['Carrinho'] = [request.POST['doce_id']]
            else:
                request.session['Carrinho'] += [request.POST['doce_id']]
        elif request.POST['tipo'] == 'remover':
            itens = request.session['Carrinho']
            itens.remove(request.POST['doce_id'])
            request.session['Carrinho'] = itens

        return redirect('carrinho')

    if request.method == 'GET':
        itens = request.session.get('Carrinho', "")
        if itens != [""]:
            itens = [get_object_or_404(Doce, pk=item) for item in itens]
            valor_total = sum([item.preco for item in itens])
        else:
            itens = None
            valor_total = 0
        return render(request, 'confeitaria/carrinho.html', {"itens": itens, "valor_total": valor_total})