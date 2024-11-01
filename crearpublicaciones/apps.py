"""
Módulo de configuración de la aplicación crearpublicaciones.

Esta clase configura la aplicación 'crearpublicaciones' dentro del proyecto IS2_Proyecto.
"""

from django.apps import AppConfig

from threading import Thread
from .tasks import verificar_inactividad_task


class CrearpublicacionesConfig(AppConfig):
    """
    Configura la aplicación 'crearpublicaciones'.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crearpublicaciones'

    def ready(self):
        import crearpublicaciones.signals
        
        
        thread = Thread(target=verificar_inactividad_task)
        thread.daemon = True
        thread.start()
