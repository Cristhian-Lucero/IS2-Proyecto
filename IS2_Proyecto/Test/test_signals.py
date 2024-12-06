from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from crearpublicaciones.models import Publicacion, Comentario, Categoria

class SignalsTestCase(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]
    def setUp(self):
        # Crear usuarios de prueba
        self.usuario1 = User.objects.get(id=1)
        self.usuario2 = User.objects.get(id=2)
        self.categoria = Categoria.objects.get(id=1)

        # Crear una publicación inicial
        self.publicacion = Publicacion.objects.create(
            titulo="Publicación de prueba",
            contenido_html="<p>Contenido inicial</p>",
            estado="borrador",
            user=self.usuario1,
            categoria=self.categoria
        )
    
    def test_notificar_cambios_publicacion(self):
        # Cambiar el estado de la publicación para activar la señal
        self.publicacion.estado = "publicado"
        self.publicacion.save()

        # Verificar que se envió un correo electrónico
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("El estado de tu publicación ha cambiado", mail.outbox[0].subject)
        self.assertIn(self.usuario1.email, mail.outbox[0].to)
    
    def test_notificar_nuevo_comentario(self):
        # Crear un comentario en la publicación
        Comentario.objects.create(
            user=self.usuario2,
            publicacion=self.publicacion,
            descripcion="Este es un comentario de prueba."
        )

        # Verificar que se envió un correo electrónico al autor de la publicación
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Nuevo comentario en tu publicación", mail.outbox[0].subject)
        self.assertIn(self.usuario1.email, mail.outbox[0].to)
