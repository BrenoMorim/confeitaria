from django.contrib import admin
from confeitaria.models import Doce, Pedido

# Register your models here.

class ListandoDoces(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "preco")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("categoria",)
    list_per_page = 15
    sortable_by = ("preco",)

class ListandoPedidos(admin.ModelAdmin):
    list_display = ("id", "nome_comprador", "contato_comprador", "valor_total", "data_pedido", "entregue")
    list_display_links = ("id", "nome_comprador")
    list_editable = ("entregue",)
    search_fields = ("nome_comprador", "contato_comprador")
    list_per_page = 15

admin.site.register(Doce, ListandoDoces)
admin.site.register(Pedido, ListandoPedidos)