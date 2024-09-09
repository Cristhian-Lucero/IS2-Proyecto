"""
Configuración de URLs para la aplicación login.

Define las rutas para la gestión de roles y categorías, así como otras funcionalidades relacionadas con la autenticación.
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio/', inicio, name='inicio'),
    path('logout/',exit,name='exit'),
    path('rol/', rol, name='rol' ),

    path('gestionrol/', gestionarRol),
    
    path('adicionrol/', agregarRol, name='adicionrol'),
    path('editar_rol/<int:rol_id>/', editarRol, name='editar_rol'),
    path('eliminar_rol/<int:rol_id>/', eliminarRol, name='eliminar_rol'),

    path('gestioncategoria/', gestionCategoria, name='gestioncategoria'),
    path('editar_categoria/<int:categoria_id>/', editarCategoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', eliminarCategoria, name='eliminar_categoria'),
]
