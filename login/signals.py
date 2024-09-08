from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Rol, Categoria, UsuarioRolCategoria

@receiver(post_save, sender=Usuario)
def asignar_rol_suscriptor(sender, instance, created, **kwargs):
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