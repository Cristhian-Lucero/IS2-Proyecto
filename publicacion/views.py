"""
Vistas de la aplicación publicacion.

Define las vistas para la creacion y listado de publicaciones.
"""

from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
#from .forms import *


# Create your views here.

from django.shortcuts import render

def crear_publicacion(request):
    """
    Renderiza la página para crear una nueva publicación.

    Returns:
        HttpResponse: Renderiza la plantilla 'publicacion/crear.html'.
    """

    return render(request, 'publicacion/crear.html')

def mis_publicaciones(request):
    """
    Muestra una lista de las publicaciones del usuario autenticado.

    Returns:
        HttpResponse: Renderiza la plantilla 'publicacion/mis_publicaciones.html'.
    """

    return render(request, 'publicacion/mis_publicaciones.html')