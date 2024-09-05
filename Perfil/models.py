from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario estándar

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)  # Subir imágenes al directorio 'media/logos'
    descripcion = models.TextField(null=True, blank=True)
    estadoUsuario = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

# Create your models here.
