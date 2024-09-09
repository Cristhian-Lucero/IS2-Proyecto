from django.db import models  # Asegúrate de que esta línea esté presente
from django.contrib.auth.models import User  # Si usas la clase User para relaciones

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField(null=True, blank=True)  
    imagen1 = models.ImageField(upload_to='uploads/', null=True, blank=True) 
    imagen2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    cita = models.TextField(null=True, blank=True)  # Campo para las citas
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'publicacion'  # Nombre de la tabla en la base de datos
