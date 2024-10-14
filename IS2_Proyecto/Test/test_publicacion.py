from django.test import TestCase
from crearpublicaciones.models import Publicacion, Comentario
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
            contenido_html = 'Contenido de prueba.',
            estado = 'borrador',
            user=usuario,  # Asociar la publicación con el usuario
            categoria=categoria  # Asociar la publicación con la categoría
        )

        # Verificar que la publicación se creó correctamente
        self.assertEqual(publicacion.titulo, 'Título de prueba')
        self.assertTrue(Publicacion.objects.filter(titulo='Título de prueba').exists())
        
    def test_publicacion_delete(self):
        # Recoger el usuario y la categoría
        usuario = User.objects.get(id=1)
        categoria = Categoria.objects.get(id=1)

        # Crear una publicación
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido_html='Contenido de prueba.',
            estado='borrador',
            user=usuario,
            categoria=categoria
        )

        # Eliminar la publicación
        publicacion_id = publicacion.id
        publicacion.delete()

        # Verificar que la publicación ya no existe
        self.assertFalse(Publicacion.objects.filter(id=publicacion_id).exists())

    def test_incrementar_vistas(self):
        # Recoger el usuario y la categoría
        usuario = User.objects.get(id=1)
        categoria = Categoria.objects.get(id=1)

        # Crear una publicación
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido_html='Contenido de prueba.',
            estado='borrador',
            user=usuario,
            categoria=categoria,
            vistas=0
        )

        # Simular que la publicación es vista 5 veces
        for _ in range(5):
            publicacion.vistas += 1
        publicacion.save()

        # Verificar que el conteo de vistas es correcto
        publicacion_refrescada = Publicacion.objects.get(id=publicacion.id)
        self.assertEqual(publicacion_refrescada.vistas, 5)
    
    def test_publicacion_likes(self):
        # Recoger el usuario y la categoría
        usuario = User.objects.get(id=1)
        categoria = Categoria.objects.get(id=1)

        # Crear una publicación
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido_html='<p>Este es el contenido HTML de la publicación.</p>',
            estado='borrador',
            user=usuario,
            categoria=categoria,
            me_gustas=0
        )

        # Simular que la publicación recibe 3 likes
        publicacion.me_gustas += 3
        publicacion.save()

        # Verificar que el conteo de likes es correcto
        publicacion_refrescada = Publicacion.objects.get(id=publicacion.id)
        self.assertEqual(publicacion_refrescada.me_gustas, 3)

    def test_agregar_comentario(self):
        # Recoger el usuario y la categoría
        usuario = User.objects.get(id=1)
        categoria = Categoria.objects.get(id=1)

        # Crear una publicación
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido_html='Contenido de prueba.',
            estado='borrador',
            user=usuario,
            categoria=categoria
        )

        # Agregar un comentario a la publicación
        comentario = Comentario.objects.create(
            user=usuario,
            publicacion=publicacion,
            descripcion="Este es un comentario de prueba."
        )

        # Verificar que el comentario se agregó correctamente
        self.assertEqual(comentario.descripcion, "Este es un comentario de prueba.")
        self.assertTrue(Comentario.objects.filter(publicacion=publicacion).exists())

    def test_cambio_estado_publicacion(self):
        # Recoger el usuario y la categoría
        usuario = User.objects.get(id=1)
        categoria = Categoria.objects.get(id=1)

        # Crear una publicación en estado 'borrador'
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido_html='Contenido de prueba.',
            estado='borrador',
            user=usuario,
            categoria=categoria
        )

        # Cambiar el estado a 'publicado'
        publicacion.estado = 'publicado'
        publicacion.save()

        # Verificar que el estado ha cambiado correctamente
        publicacion_refrescada = Publicacion.objects.get(id=publicacion.id)
        self.assertEqual(publicacion_refrescada.estado, 'publicado')

