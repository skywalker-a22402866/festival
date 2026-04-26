from django.contrib import admin
from .models import Dia, Concerto, Banda, Palco

admin.site.register(Banda)
admin.site.register(Dia)
admin.site.register(Palco)
admin.site.register(Concerto)
