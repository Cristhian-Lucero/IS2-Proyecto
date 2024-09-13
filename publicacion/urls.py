"""
Definición de URLs para la aplicación 'publicacion'.

Este módulo establece los patrones de URL para las vistas relacionadas con la creación y gestión
de publicaciones por parte del usuario. Incluye rutas para crear nuevas publicaciones y
ver las publicaciones propias del usuario.
"""

from django.urls import include, path
from .views import *
from . import views

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('mis/', views.mis_publicaciones, name='mis_publicaciones'),
]

