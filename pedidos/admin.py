from django.contrib import admin
from pedidos.models import Pedido


class ListandoPedidos(admin.ModelAdmin):
    list_display = ("id", "nome_comprador", "contato_comprador", "valor_total", "data_pedido", "data_entrega", "entregue")
    list_display_links = ("id", "nome_comprador", "contato_comprador")
    list_editable = ("entregue",)
    list_filter = ("data_pedido", "data_entrega", "entregue")
    search_fields = ("nome_comprador", "contato_comprador")
    list_per_page = 15

admin.site.register(Pedido, ListandoPedidos)
