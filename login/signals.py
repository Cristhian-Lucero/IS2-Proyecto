from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Rol, Categoria, UsuarioRolCategoria

@receiver(post_save, sender=Usuario)
def asignar_rol_suscriptor(sender, instance, created, **kwargs):
    """
    Asigna el rol 'Suscriptor' (con id=5) a todas las categorías cuando se crea un nuevo usuario.

    Argumentos:
        sender (Model class): El modelo que envió la señal, en este caso, 'Usuario'.
        instance (Usuario): La instancia del modelo 'Usuario' que se acaba de crear.
        created (bool): Valor booleano que indica si la instancia fue creada (True) o actualizada (False).
        **kwargs: Parámetros adicionales.

    Retorna:
        None: La función no retorna un valor, pero crea registros en la tabla 'UsuarioRolCategoria'.
    """
    if created:
        # Obtén el rol con id 5
        rol_suscriptor = Rol.objects.get(id=5)
        # Obtén todas las categorías
        categorias = Categoria.objects.all()
        # Crea una instancia de UsuarioRolCategoria para cada categoría
        for categoria in categorias:
            UsuarioRolCategoria.objects.create(
                usuario=instance, 
                rol=rol_suscriptor,
                categoria=categoria
            )