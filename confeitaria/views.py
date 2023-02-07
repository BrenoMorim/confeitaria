from django.shortcuts import render, redirect
from confeitaria.models import Doce, CATEGORIAS
from django.shortcuts import get_object_or_404
from django.contrib import messages

def index(request):

    doces_baratos = Doce.objects.filter(preco__lt=20.0)[:10]
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
        
        # Adiciona item no carrinho através das sessões do Django
        if request.POST['tipo'] == 'adicionar':
            if not 'Carrinho' in request.session.keys():
                request.session['Carrinho'] = [request.POST['doce_id']]
            else:
                request.session['Carrinho'] += [request.POST['doce_id']]
            messages.success(request, "Doce adicionado ao carrinho com sucesso!")

        # Remove o item da lista do carrinho
        elif request.POST['tipo'] == 'remover':
            itens = request.session['Carrinho']
            itens.remove(request.POST['doce_id'])
            request.session['Carrinho'] = itens
            messages.success(request, "Doce removido do carrinho com sucesso!")

        return redirect('carrinho')

    if request.method == 'GET':

        # A sessão armazena somente os ids dos produtos
        itens = request.session.get('Carrinho', "")
        if itens != [""]:
            # Então é preciso buscar o resto dos dados no banco de dados
            itens = [get_object_or_404(Doce, pk=item) for item in itens]
            valor_total = sum([item.preco for item in itens])
        else:
            itens = None
            valor_total = 0
        return render(request, 'confeitaria/carrinho.html', {"itens": itens, "valor_total": valor_total})

def erro404(request, exception):
    return render(request, 'erro.html', {"mensagem": "Ops! A página que você buscou não foi encontrada =("}, status=404)

def erro500(request):
    return render(request, 'erro.html', {"mensagem": "Ops! Aconteceu um erro inesperado no nosso servidor =("}, status=500)