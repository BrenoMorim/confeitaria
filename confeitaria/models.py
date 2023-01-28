from django.db import models
from django.core.validators import MinValueValidator

class Doce(models.Model):
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

    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(max_length=255, null=False, blank=False)
    categoria = models.CharField(max_length=30, null=False, blank=False, default='', choices=CATEGORIAS)
    preco = models.FloatField(null=False, validators=[MinValueValidator(0.10)])
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
