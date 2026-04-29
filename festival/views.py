from django.shortcuts import render, get_object_or_404
from .models import Concerto, Dia, Palco


def index_view(request):
    return render(request, 'festival/index.html')


# LISTA DE DIAS
def dias_view(request):
    dias = Dia.objects.all()
    return render(request, 'festival/dias.html', {'dias': dias})


# DETALHE DE UM DIA
def dia_detail_view(request, id):
    dia = get_object_or_404(Dia, id=id)
    return render(request, 'dia_detail.html', {'dia': dia})


def concerto_view(request, id):
    concerto = get_object_or_404(Concerto, id=id)
    return render(request, 'festival/concerto.html', {'concerto': concerto})

def palcos_view(request):
    palcos = Palco.objects.all()

    return render(request, 'festival/palcos.html', {'palcos': palcos})