from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Pedido(models.Model):
    nome_comprador = models.CharField(max_length=60, null=False, blank=False)
    contato_comprador = models.CharField(max_length=20, null=False, blank=False)
    valor_total = models.FloatField(validators=[MinValueValidator(0.10)])
    cep_entrega = models.CharField(max_length=9, null=False, blank=False)
    numero_endereco = models.PositiveIntegerField(null=False)
    itens = models.JSONField(null=False)
    entregue = models.BooleanField(default=False)
    data_pedido = models.DateField(default=timezone.now)
    data_entrega = models.DateField(blank=False, null=False)
