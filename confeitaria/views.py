from django.shortcuts import render, redirect
from confeitaria.models import Doce, Pedido, CATEGORIAS
from confeitaria.forms import PedidoForms
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

        if request.POST['tipo'] == 'adicionar':
            if not 'Carrinho' in request.session.keys():
                request.session['Carrinho'] = [request.POST['doce_id']]
            else:
                request.session['Carrinho'] += [request.POST['doce_id']]
            messages.info(request, "Doce adicionado ao carrinho com sucesso!")

        elif request.POST['tipo'] == 'remover':
            itens = request.session['Carrinho']
            itens.remove(request.POST['doce_id'])
            messages.info(request, "Doce removido do carrinho com sucesso!")
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

def finalizar_pedido(request):

    itens = request.session.get('Carrinho', "")
    if itens == [""] or not itens:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('carrinho')

    itens = [get_object_or_404(Doce, pk=item) for item in itens]
    itens = [{"id": item.id, "nome": item.nome, "preco": item.preco} for item in itens]
    
    valor_total = sum([item['preco'] for item in itens])
    
    forms = PedidoForms()
    
    if request.method == 'POST':
        forms = PedidoForms(request.POST)
        
        if forms.is_valid():
            nome = forms['nome'].value()
            contato = forms['contato'].value()
            cep = forms['cep'].value()
            numero_endereco = forms['numero_endereco'].value()

            pedido = Pedido.objects.create(
                nome_comprador=nome,
                contato_comprador=contato,
                valor_total=valor_total,
                cep_entrega=cep,
                numero_endereco=numero_endereco,
                itens = {"itens": itens}
            )

            pedido.save()
            request.session['Carrinho'] = []
            messages.success(request, 'Pedido finalizado com sucesso! Entraremos em contato em breve para mais detalhes')
            return redirect('index')

    return render(request, "confeitaria/finalizar-pedido.html", {"form": forms, "valor_total": valor_total})
