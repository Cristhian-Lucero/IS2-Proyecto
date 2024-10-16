from django.db.models.signals import post_save, pre_delete
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
        kwargs: Parámetros adicionales.

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
    
@receiver(post_save, sender=Categoria)
def asignar_rol_a_usuarios(sender, instance, created, **kwargs):
    if created:
        # Obtener el rol "Suscriptor"
        suscriptor_rol = Rol.objects.get(nombre='Suscriptor')

        # Obtener todos los usuarios
        usuarios = Usuario.objects.all()

        # Crear una relación UsuarioRolCategoria para cada usuario con la nueva categoría
        for usuario in usuarios:
            UsuarioRolCategoria.objects.create(
                usuario=usuario,
                rol=suscriptor_rol,
                categoria=instance
            )

@receiver(pre_delete, sender=Rol)
def actualizar_usuarios_tras_eliminar_rol(sender, instance, **kwargs):
    """
    Cambia el rol de los usuarios a 'Suscriptor' cuando se elimina un rol.
    """
    # Obtenemos el rol que se está eliminando
    rol_eliminado = instance
    
    # Buscamos el rol 'Suscriptor' (asegurándonos de que existe)
    try:
        suscriptor = Rol.objects.get(nombre='Suscriptor')
    except Rol.DoesNotExist:
        print("El rol 'Suscriptor' no existe. Por favor, créalo primero.")
        return  # Detenemos la ejecución si no existe el rol 'Suscriptor'
    
    # Encontramos los usuarios que tenían el rol que se va a eliminar
    usuarios_a_modificar = UsuarioRolCategoria.objects.filter(rol=rol_eliminado)
    
    # Actualizamos los usuarios para que ahora pertenezcan al rol 'Suscriptor'
    for usuario in usuarios_a_modificar:
        usuario.rol = suscriptor  # Asignamos el rol 'Suscriptor'
        usuario.save()