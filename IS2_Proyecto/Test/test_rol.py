import pytest
from login.models import Rol, Permiso


@pytest.mark.django_db
def test_rol_creation():
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
