from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.contrib.auth.models import User

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField()
    imagen1 = models.ImageField(upload_to='imagenes/', null=False, blank=False)
    imagen2 = models.ImageField(upload_to='imagenes/', null=True, blank=True)  # Opcional
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Relación con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Este es el campo faltante

    def __str__(self):
        return self.titulo


