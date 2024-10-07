from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Usuario

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil de Usuario asociado cada vez que se crea un nuevo User.

    Attributes:
        sender (Model): La clase del modelo que envía la señal (User).
        instance (User): La instancia del modelo User que se ha guardado.
        created (bool): Indica si se ha creado una nueva instancia.
        **kwargs: Parámetros adicionales clave-valor.
    """

    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guarda el perfil de Usuario asociado cada vez que se guarda un User.

    Attributes:
        sender (Model): La clase del modelo que envía la señal (User).
        instance (User): La instancia del modelo User que se ha guardado.
        **kwargs: Parámetros adicionales clave-valor.
    """

    instance.usuario.save()

