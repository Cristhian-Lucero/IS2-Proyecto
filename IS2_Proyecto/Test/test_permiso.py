import pytest
from login.models import Permiso


@pytest.mark.django_db
def test_permiso_creation():
    # se crea una nueva categoria
    permiso = Permiso.objects.create(
        nombre="nombre de prueba",
        descripcion="Descripción de prueba",
    )

    # se verifica que la categoria fue creada correctamente
    assert permiso.nombre == "nombre de prueba"
    assert permiso.descripcion == "Descripción de prueba"