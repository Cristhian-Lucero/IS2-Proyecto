"""
Configuración del panel de administración para el módulo login.

Registra los modelos Permiso, Rol y Categoria en el panel de administración de Django
para que puedan ser gestionados a través de la interfaz de administrador.
"""

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Permiso)
admin.site.register(Rol)
admin.site.register(Categoria)
