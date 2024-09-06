from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from django.db import models

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField()
    imagen1 = models.ImageField(upload_to='imagenes/', null=False, blank=False)
    imagen2 = models.ImageField(upload_to='imagenes/', null=True, blank=True)  # Esta es opcional
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones_crear')

    def __str__(self):
        return self.titulo
