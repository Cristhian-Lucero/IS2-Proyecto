"""
Configuración de la aplicación 'publicacion'.

Este módulo define la configuración de la aplicación 'publicacion' y puede ser utilizado para inicializar
la configuración específica de la aplicación o registrar señales cuando la aplicación esté lista.
"""

from django.apps import AppConfig


class PublicacionConfig(AppConfig):
    """
    Configuración de la aplicación 'publicacion'.

    Esta clase configura la aplicación 'publicacion' y puede ser utilizada para inicializar
    la configuración de la aplicación o registrar señales cuando la aplicación está lista.

    Atributos:
        default_auto_field (str): Especifica el tipo de campo automático por defecto para los modelos.
        name (str): Nombre de la aplicación.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publicacion'
