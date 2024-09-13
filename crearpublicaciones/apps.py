"""
Módulo de configuración de la aplicación crearpublicaciones.

Esta clase configura la aplicación 'crearpublicaciones' dentro del proyecto IS2_Proyecto.
"""

from django.apps import AppConfig


class CrearpublicacionesConfig(AppConfig):
    """
    Configura la aplicación 'crearpublicaciones'.
    
    Atributos:
        default_auto_field (str): Tipo de campo auto-incremental ('BigAutoField').
        name (str): Nombre de la aplicación ('crearpublicaciones').
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crearpublicaciones'
