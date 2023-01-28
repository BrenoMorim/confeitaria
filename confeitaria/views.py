from django.shortcuts import render
from confeitaria.models import Doce

# Create your views here.

def index(request):
    doces = Doce.objects.all()
    return render(request, "confeitaria/index.html", {"doces": doces})
