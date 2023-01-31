from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

CATEGORIAS = [
    ("BRIGADEIRO", "Brigadeiro"),
    ("BOLO", "Bolo"),
    ("PUDIM", "Pudim"),
    ("MOUSSE", "Mousse"),
    ("PAVÊ", "Pavê"),
    ("SORVETE", "Sorvete"),
    ("AÇAÍ", "Açaí"),
    ("BEIJINHO", "Beijinho"),
    ("BROWNIE", "Brownie"),
    ("OUTROS", "Outros")
]

class Doce(models.Model):

    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(max_length=255, null=False, blank=False)
    categoria = models.CharField(max_length=30, null=False, blank=False, default='', choices=CATEGORIAS)
    preco = models.FloatField(null=False, validators=[MinValueValidator(0.10)])
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)

class Pedido(models.Model):
    nome_comprador = models.CharField(max_length=60, null=False, blank=False)
    contato_comprador = models.CharField(max_length=20, null=False, blank=False)
    valor_total = models.FloatField(validators=[MinValueValidator(0.10)])
    cep_entrega = models.CharField(max_length=9, null=False, blank=False)
    numero_endereco = models.PositiveIntegerField(null=False)
    itens = models.JSONField(null=False)
    entregue = models.BooleanField(default=False)
    data_pedido = models.DateField(default=datetime.now())
