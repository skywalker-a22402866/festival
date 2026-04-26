from django.shortcuts import render
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
    concerto = Concerto.objects.all()

    context = {'concerto': concerto}

    return render(request, 'festival/concerto.html', context)

def palcos_view(request, id):
    palco = Palco.objects.get(id=id)

    return render(request, 'festival/palcos.html', {'palcos': palco})