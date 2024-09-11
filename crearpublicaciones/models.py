from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField(null=True, blank=True)  
    imagen1 = models.ImageField(upload_to='uploads/', null=True, blank=True) 
    imagen2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
