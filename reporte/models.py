from django.db import models

# Create your models here.

class Reporte(models.Model):
    """
    
    """

    TIPO_CHOICES = [
        ('alcance', 'Alcance'),
        ('mas likeado', 'Mas likeado'),
        ('mas leido', 'Mas leido'),
        ('publicado por tiempo', 'Publicado por tiempo'),
        ('redactado por tiempo', 'Redactado por tiempo'),
        ('tiempo de revision', 'Tiempo de revision'),
        ('articulos inactivados por tiempo', 'Articulos inactivados por tiempo'),
    ]

    titulo = models.CharField(max_length=200)
    html_content = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    
    def __str__(self):
        return self.titulo
