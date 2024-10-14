"""
Configuración de URLs para la aplicación Perfil.

Define las rutas para la gestión de perfiles.
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', PerfilDetailView.as_view(), name='ver_perfil'),
    path('perfil/', perfil_update, name='perfil'),
]

