import pytest
from login.models import Categoria


@pytest.mark.django_db
def test_categoria_creation():
    # se crea una nueva categoria
    categoria = Categoria.objects.create(
        descripcion_corta="Descripción corta de prueba",
        descripcion_larga="Descripción larga de prueba",
        estado="Activo"
    )

    # se verifica que la categoria fue creada correctamente
    assert categoria.descripcion_corta == "Descripción corta de prueba"
    assert categoria.descripcion_larga == "Descripción larga de prueba"
    assert categoria.estado == "Activo"
