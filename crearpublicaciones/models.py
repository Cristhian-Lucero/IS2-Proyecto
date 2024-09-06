from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField()
    imagen1 = models.ImageField(upload_to='imagenes/')
    imagen2 = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

