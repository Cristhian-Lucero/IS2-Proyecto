from django.apps import AppConfig


class PerfilConfig(AppConfig):
    """
    Configuración de la aplicación 'Perfil'.

    Esta clase configura la aplicación 'Perfil' y se encarga de registrar las señales
    definidas en 'Perfil.signals' cuando la aplicación está lista.

    Atributos:
        default_auto_field (str): Especifica el tipo de campo automático por defecto para los modelos.
        name (str): Nombre de la aplicación.
    Métodos:
        ready(): Método llamado cuando la aplicación está lista. Importa el módulo de señales.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Perfil'
class PerfilConfig(AppConfig):
    name = 'Perfil'

    def ready(self):
        import Perfil.signals  # Importa las señales