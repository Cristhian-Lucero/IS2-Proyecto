"""
Modelos de la aplicación login.

Contiene los modelos:
- Permiso: Define permisos específicos.
- Rol: Relaciona roles con permisos.
- Categoria: Define las categorías para gestionar publicaciones u otros elementos.
- UsuarioRolCategoria: Relaciona usuarios, roles y categorías.
"""

from django.db import models
from Perfil.models import Usuario

class Permiso(models.Model):
    """
    Modelo que representa un permiso en el sistema.

    Un permiso define una acción específica o acceso que puede ser otorgado a los roles de usuario.

    Atributos:
        nombre (CharField): Nombre único que identifica el permiso. Máximo 100 caracteres.
        descripcion (TextField): Descripción detallada del permiso y su funcionalidad.

    Métodos:
        __str__(): Retorna el nombre del permiso como representación en cadena del objeto.
    """

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    """
    Modelo que representa un rol de usuario en el sistema.

    Un rol es una colección de permisos que define lo que un usuario puede hacer dentro del sistema.

    Atributos:
        nombre (CharField): Nombre único que identifica el rol. Máximo 25 caracteres.
        descripcion (TextField): Descripción detallada del rol y sus responsabilidades.
        permisos (ManyToManyField): Relación con Permiso, indicando los permisos asociados al rol.

    Métodos:
        __str__(): Retorna el nombre del rol como representación en cadena del objeto.
    """

    nombre = models.CharField(max_length=25)
    descripcion = models.TextField()
    permisos = models.ManyToManyField(Permiso, related_name='roles')

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    """
    Modelo que representa una categoría para gestionar publicaciones u otros elementos.

    Las categorías se utilizan para organizar y clasificar elementos dentro del sistema.

    Atributos:
        descripcion_corta (CharField): Descripción breve de la categoría. Máximo 100 caracteres.
        descripcion_larga (TextField): Descripción detallada de la categoría.
        estado (CharField): Estado actual de la categoría (e.g., 'Activo', 'Inactivo'). Máximo 50 caracteres.

    Métodos:
        __str__(): Retorna la descripción corta como representación en cadena del objeto.
    """

    descripcion_corta = models.CharField(max_length=100)
    descripcion_larga = models.TextField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_corta

class UsuarioRolCategoria(models.Model):
    """
    Modelo que representa la relación entre un Usuario, un Rol y una Categoría.

    Este modelo vincula un usuario específico con un rol determinado dentro de una categoría específica.
    Se asegura que la combinación de usuario, rol y categoría sea única, evitando duplicados.

    Atributos:
        usuario (ForeignKey): Referencia al modelo Usuario. Indica el usuario asociado.
        rol (ForeignKey): Referencia al modelo Rol. Indica el rol del usuario en la categoría.
        Por defecto, se asigna el rol con nombre 'Suscriptor'.
        categoria (ForeignKey): Referencia al modelo Categoria. Indica la categoría asociada.

    Meta:
        unique_together = ('usuario', 'rol', 'categoria'): Garantiza la unicidad de la combinación.
        verbose_name = 'Usuario Rol Categoria'
        verbose_name_plural = 'Usuarios Roles Categorías'

    Métodos:
        __str__(): Retorna una representación en cadena del objeto en el formato 'usuario - rol - categoría'.
    """

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)  # Rol por defecto
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.rol_id:  # Si no se ha asignado un rol aún
            self.rol = Rol.objects.get(nombre='Suscriptor')
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('usuario', 'rol', 'categoria')  # Asegura que no se repita la misma combinación
        verbose_name = 'Usuario Rol Categoria'
        verbose_name_plural = 'Usuarios Roles Categorías'

    def __str__(self):
        return f'{self.usuario} - {self.rol} - {self.categoria}'

