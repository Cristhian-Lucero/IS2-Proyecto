"""
Configuración del panel de administración para el módulo Perfil.

Registra el modelo Usuario en el panel de administración de Django
para que pueda ser gestionado a través de la interfaz de administrador.
"""

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Usuario)