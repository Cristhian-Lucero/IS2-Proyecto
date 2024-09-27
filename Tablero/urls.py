"""
URLs de la aplicación 'Tableros'.

Este archivo define las rutas de URL para gestionar el tablero Kanban
"""

from django.urls import path
from .views import *

urlpatterns = [
    # Ruta sin categoría seleccionada (carga la primera categoría activa por defecto)
    path('index/', kanban_board, name='kanban_board'), 

    # Ruta con categoría seleccionada
    path('index/<int:categoria_id>/', kanban_board, name='kanban_board'),
]

