from django.contrib import admin
from confeitaria.models import Doce

# Register your models here.

class ListandoDoces(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "preco")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("categoria",)
    list_per_page = 15
    sortable_by = ("preco",)

admin.site.register(Doce, ListandoDoces)