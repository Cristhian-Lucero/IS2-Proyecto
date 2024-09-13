"""
Módulo de administración para el modelo 'Publicacion'.

Este módulo registra el modelo 'Publicacion' en el sitio de administración
de Django, lo que permite gestionar las publicaciones desde la interfaz
de administración predeterminada.
"""


from django.contrib import admin
from .models import Publicacion

# Register your models here.
admin.site.register(Publicacion)

