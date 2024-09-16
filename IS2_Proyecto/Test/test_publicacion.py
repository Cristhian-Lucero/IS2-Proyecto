from django.test import TestCase
from crearpublicaciones.models import Publicacion
from django.contrib.auth.models import User
from login.models import Categoria

class PublicacionCreationTest(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]

    def test_publicacion_creation(self):
        # Recoger el usuario con id=1
        usuario = User.objects.get(id=1)

        # Recoger la categoría con id=1
        categoria = Categoria.objects.get(id=1)

        # Crear la publicación asociada al usuario y a la categoría
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            texto_corto='Este es el texto corto de la publicación.',
            texto_largo='Este es el texto largo de la publicación.',
            cita='Esto es una cita de la publicacion',
            user=usuario,  # Asociar la publicación con el usuario
            categoria=categoria  # Asociar la publicación con la categoría
        )

        # Verificar que la publicación se creó correctamente
        self.assertEqual(publicacion.titulo, 'Título de prueba')
        self.assertTrue(Publicacion.objects.filter(titulo='Título de prueba').exists())
