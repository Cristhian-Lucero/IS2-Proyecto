from django.db import models
"""
Modelos de la aplicación login.

Contiene los modelos:
- Permiso: Define permisos específicos.
- Rol: Relaciona roles con permisos.
- Categoria: Define las categorías para gestionar publicaciones u otros elementos.
- Usuario: Define los usuarios del sistema con sus atributos.
"""

class Permiso(models.Model):
    """
    Modelo que representa un permiso en el sistema.

    Un permiso tiene un nombre y una descripción.
    """

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    """
    Modelo que representa un rol de usuario.

    Un rol está compuesto por un nombre, una descripción y está relacionado con varios permisos.
    """

    nombre = models.CharField(max_length=25)
    descripcion = models.TextField()
    permisos = models.ManyToManyField(Permiso, related_name='roles')

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    """
    Modelo que representa una categoría para gestionar publicaciones o elementos.

    Una categoría tiene una descripción corta, descripción larga y un estado (activo o inactivo).
    """

    descripcion_corta = models.CharField(max_length=100)
    descripcion_larga = models.TextField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_corta

class Usuario(models.Model):
    """
    Modelo que representa un usuario en el sistema.

    Un usuario tiene un nombre que se guarda en este modelo.
    """
    Nombre = models.CharField(max_length=100)