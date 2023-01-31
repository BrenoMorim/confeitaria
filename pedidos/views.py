from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from confeitaria.models import Doce
from pedidos.models import Pedido
from pedidos.forms import PedidoForms


def finalizar_pedido(request):

    itens = request.session.get('Carrinho', "")
    # O pedido não pode ser finalizado se o carrinho estiver vazio
    if itens == [""] or not itens:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('carrinho')

    itens = [get_object_or_404(Doce, pk=item) for item in itens]

    # Recupera somente as informações mais importantes: Nome, preço e id
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
            data_entrega = forms['data_entrega'].value()

            # Adaptando a data para o formato aceito pelo banco de dados
            dia, mes, ano = data_entrega.split('/')
            data_entrega = f"{ano}-{mes}-{dia}"

            pedido = Pedido.objects.create(
                nome_comprador=nome,
                contato_comprador=contato,
                valor_total=valor_total,
                cep_entrega=cep,
                numero_endereco=numero_endereco,
                itens={"itens": itens},
                data_entrega=data_entrega
            )

            pedido.save()
            request.session['Carrinho'] = []
            messages.success(request, 'Pedido finalizado com sucesso! Entraremos em contato em breve para mais detalhes')
            return redirect('index')

    return render(request, "pedidos/finalizar-pedido.html", {"form": forms, "valor_total": valor_total})
