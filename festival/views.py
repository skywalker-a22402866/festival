from django.shortcuts import render
from .models import Palco


def index_view(request):
    return render(request, 'festival/index.html')


def dias_view(request):
    dias = Dia.objects.all() 

    context = {'dias': dias}

    return render(request, 'festival/dias.html', context)



def concerto_view(request, id):
    concerto = 

    context = {'concerto': concerto}

    return render(request, 'festival/concerto.html', context)