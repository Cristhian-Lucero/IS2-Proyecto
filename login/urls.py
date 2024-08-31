from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio/', inicio, name='inicio'),
    path('base/', base, name='base'),
    path('base2/', base2, name='base2'),
    path('logout/',exit,name='exit'),
    path('gestionrol/', gestionarRol),
    path('adicionrol/', agregarRol),
    path('gestioncategoria/', gestionCategoria),
]
