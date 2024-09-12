from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
#from .forms import *


# Create your views here.

from django.shortcuts import render

def crear_publicacion(request):
    # lógica para crear una publicación
    return render(request, 'publicacion/crear.html')

def mis_publicaciones(request):
    # lógica para listar las publicaciones del usuario
    return render(request, 'publicacion/mis_publicaciones.html')