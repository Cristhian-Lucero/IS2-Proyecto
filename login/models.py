from django.db import models
from Perfil.models import Usuario

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

class UsuarioRolCategoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=lambda: Rol.objects.get(nombre='Suscriptor'))  # Rol por defecto
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'rol', 'categoria')  # Asegura que no se repita la misma combinación
        verbose_name = 'Usuario Rol Categoria'
        verbose_name_plural = 'Usuarios Roles Categorías'

    def __str__(self):
        return f'{self.usuario} - {self.rol} - {self.categoria}'