"""
URLs de la aplicación 'Tableros'.

Este archivo define las rutas de URL para gestionar el tablero Kanban
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('update_task_state/<int:task_id>/', update_task_state, name='update_task_state'),
    path('index/', kanban_board, name='kanban_board'), 
    path('index/<int:categoria_id>/', kanban_board, name='kanban_board'),
]

