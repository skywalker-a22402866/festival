from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('palcos/<int:id>', views.palcos_view, name='palcos'),
    path('concertos/<int:id>/', views.concerto_view, name='concerto'),
    path('dias/', views.dias_view, name='dias'),              # lista de dias
    path('dias/<int:id>/', views.dia_detail_view, name='dia'),  # detalhe de 1 dia
]
