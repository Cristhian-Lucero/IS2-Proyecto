import pytest
from login.models import Categoria, Rol

@pytest.mark.django_db
def test_categoria_creation():
    #categoria necesita rol base Suscriptor
    suscriptor_rol = Rol.objects.create(nombre='Suscriptor')

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

@pytest.mark.django_db
def test_categoria_delete():
    #categoria necesita rol base Suscriptor
    Rol.objects.create(nombre='Suscriptor')

    # se crea una nueva categoria
    categoria = Categoria.objects.create(
        descripcion_corta="Descripción corta de prueba",
        descripcion_larga="Descripción larga de prueba",
        estado="Activo"
    )
    categoria_id = categoria.id
    categoria.delete()


    # se verifica que la categoria fue creada correctamente
    assert Categoria.objects.filter(pk=categoria_id).exists() == False