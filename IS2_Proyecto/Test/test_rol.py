from django.test import TestCase
from unittest import skip
from django.contrib.auth.models import User
from login.models import Rol, Permiso, UsuarioRolCategoria, Categoria, Usuario

class RolTest(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]

    def test_rol_creation(self):
        # Crear el objeto Rol
        rol = Rol.objects.create(
            nombre='Nombre de prueba',
            descripcion='descripcion de prueba',
        )

        # Asignar los permisos
        permiso_de_prueba = Permiso.objects.create(nombre='permiso de prueba',descripcion="Descripción de prueba",)
        rol.permisos.add(permiso_de_prueba)

        assert rol.nombre == 'Nombre de prueba'
        assert rol.permisos.filter(nombre='permiso de prueba').exists()