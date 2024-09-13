from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario estándar

class Usuario(models.Model):
    """
    Modelo que extiende el modelo de usuario estándar de Django para añadir información adicional.

    Este modelo utiliza una relación Uno a Uno con el modelo `User` de Django para almacenar
    información adicional sobre el usuario, como su logo, descripción y estado.

    Atributos:
        user (OneToOneField): Relación uno a uno con el modelo `User`. Indica el usuario asociado.
            `on_delete=models.CASCADE` asegura que cuando se elimine el usuario estándar, también
            se eliminará la instancia asociada de `Usuario`.
        logo (ImageField): Campo opcional para almacenar una imagen de logo asociada al usuario.
            Las imágenes se subirán al directorio `media/logos/`. Permite valores nulos y en blanco.
        descripcion (TextField): Campo opcional para almacenar una descripción del usuario.
            Permite valores nulos y en blanco.
        estadoUsuario (CharField): Campo opcional para indicar el estado del usuario.
            Máximo 50 caracteres. Permite valores nulos y en blanco.

    Métodos:
        __str__(): Retorna el nombre de usuario (`username`) del usuario asociado.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)  # Subir imágenes al directorio 'media/logos'
    descripcion = models.TextField(null=True, blank=True)
    estadoUsuario = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

# Create your models here.
