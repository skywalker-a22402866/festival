from django.shortcuts import render
from .models import Concerto, Dia, Palco


def index_view(request):
    return render(request, 'festival/index.html')


def dias_view(request, id):
    dias = Dia.objects.all() 

    context = {'dias': dias}

    return render(request, 'festival/dias.html', context)



def concerto_view(request, id):
    concerto = Concerto.objects.All()

    context = {'concerto': concerto}

    return render(request, 'festival/concerto.html', context)

def palcos_view(request, id):
    palco = Palco.objects.All()

    context = {'Palcos': palco}

    return render(request, 'festival/palco.html', context)