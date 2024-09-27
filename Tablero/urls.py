"""
URLs de la aplicación 'Tableros'.

Este archivo define las rutas de URL para gestionar el tablero Kanban
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('index/',kanban_board, name='index'),
]

