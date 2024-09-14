"""
Modelo de la aplicación para gestionar las publicaciones de los usuarios.

"""

from django.db import models  # Asegúrate de que esta línea esté presente
from django.contrib.auth.models import User  # Si usas la clase User para relaciones
from login.models import Categoria

class Publicacion(models.Model):
    """
    Modelo que representa una publicación en el sistema.

    Atributos:
        titulo (CharField): El título de la publicación (máximo 200 caracteres).
        texto_corto (TextField): Resumen breve o descripción corta de la publicación.
        texto_largo (TextField): Contenido más extenso de la publicación (opcional).
        imagen1, imagen2 (ImageField): Imágenes opcionales que el usuario puede subir.
        cita (TextField): Cita opcional relacionada con la publicación.
        user (ForeignKey): Relación con el modelo User, indicando el autor.
        fecha_creacion (DateTimeField): Fecha y hora de creación de la publicación.
    """
    
    titulo = models.CharField(max_length=200)
    texto_corto = models.TextField()
    texto_largo = models.TextField(null=True, blank=True)  
    imagen1 = models.ImageField(upload_to='uploads/', null=True, blank=True) 
    imagen2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    cita = models.TextField(null=True, blank=True)  # Campo para las citas
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    ############################ PARTE DE IVAN ############################
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.categoria_id:  # Si no se ha asignado un rol aún
            self.categoria = Categoria.objects.get(id=1)
        super().save(*args, **kwargs)

    #######################################################################

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'publicacion'  # Nombre de la tabla en la base de datos
