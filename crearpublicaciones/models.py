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
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
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

class Historial(models.Model):
    ACCION_CHOICES = [
        ('creado', 'Creado'),
        ('modificado', 'Modificado'),
        ('cambio_estado', 'Cambio de Estado'),
        ('eliminado', 'Eliminado'), # El elimnado puede no ser necesario
        ('inactivado', 'Inactivado')
    ]

    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_evento = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    estado_anterior = models.CharField(max_length=10, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.publicacion.titulo} - {self.accion} - {self.fecha_evento}"

    class Meta:
        db_table = 'historial_publicacion'
        ordering = ['-fecha_evento']