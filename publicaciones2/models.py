from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    encabezado = models.CharField(max_length=255)
    cuerpo = models.TextField()
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.encabezado
    