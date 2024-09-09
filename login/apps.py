"""
Configuración de la aplicación login.

Esta clase configura la aplicación 'login' dentro del proyecto IS2_Proyecto.
"""

from django.apps import AppConfig


class LoginConfig(AppConfig):
    """
    Configuración de la aplicación login.

    Esta clase define la configuración básica de la aplicación login, incluyendo su nombre y campo de ID predeterminado.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
