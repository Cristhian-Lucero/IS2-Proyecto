"""
Modelo de la aplicación para gestionar las publicaciones de los usuarios.

"""

from django.db import models
from django.contrib.auth.models import User
from login.models import Categoria

class Publicacion(models.Model):
    """
    Modelo que representa una publicación en el sistema.
    """
    
    # Definición de estados posibles para la publicación
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('revision', 'En Revisión'),
        ('rechazado', 'Rechazado'),
        ('publicado', 'Publicado'),
    ]

    titulo = models.CharField(max_length=200)
    contenido_html = models.TextField()  # Campo para almacenar el contenido HTML completo
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    vistas = models.IntegerField(default=0)
    me_gustas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'publicacion'

class Likes(models.Model):
    """
    Modelo que representa un 'me gusta' de un usuario a una publicación.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    

class Comentario(models.Model):
    """
    Modelo que representa un comentario de un usuario en una publicación.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.publicacion.titulo} - {self.fecha_creacion}'

