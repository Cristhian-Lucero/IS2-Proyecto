from django.db import models

class Permiso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.TextField()
    permisos = models.ManyToManyField(Permiso, related_name='roles')

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    descripcion_corta = models.CharField(max_length=100)
    descripcion_larga = models.TextField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_corta

class Usuario(models.Model):
    Nombre = models.CharField(max_length=100)