from django.apps import AppConfig


class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Perfil'
class PerfilConfig(AppConfig):
    name = 'Perfil'

    def ready(self):
        import Perfil.signals  # Importa las señales