import pytest
from login.models import Usuario


@pytest.mark.django_db
def test_user_creation():
    # e crea un nuevo usuario
    usuario = Usuario.objects.create(
        Nombre = 'prueba'
    )

    # se verifica que el usuario fue creado correctamente
    assert usuario.Nombre == "prueba"