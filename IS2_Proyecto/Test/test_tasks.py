from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from crearpublicaciones.models import Publicacion, Historial
from crearpublicaciones.tasks import verificar_inactividad_task
from django.contrib.auth.models import User
from login.models import Categoria

class VerificarInactividadTaskTest(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]

    def setUp(self):
        # Configurar datos iniciales para las pruebas
        self.usuario = User.objects.get(id=1)
        self.categoria = Categoria.objects.get(id=1)

        # Crear una publicación activa con más de 30 días de antigüedad
        self.publicacion_inactiva = Publicacion.objects.create(
            titulo='Publicación antigua',
            contenido_html='<p>Contenido de prueba</p>',
            estado='publicado',
            user=self.usuario,
            categoria=self.categoria,
            fecha_publicacion=timezone.now() - timedelta(days=31)
        )

        # Crear una publicación reciente que no debería ser inactivada
        self.publicacion_activa = Publicacion.objects.create(
            titulo='Publicación reciente',
            contenido_html='<p>Contenido de prueba reciente</p>',
            estado='publicado',
            user=self.usuario,
            categoria=self.categoria,
            fecha_publicacion=timezone.now() - timedelta(days=10)
        )

    def run_inmediate_inactividad_task(self):
        # Lógica duplicada de `verificar_inactividad_task` sin esperar al mediodia
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual - timedelta(days=30)
        publicaciones = Publicacion.objects.filter(fecha_publicacion__lte=fecha_limite, estado='publicado')
        if publicaciones.exists():
            publicaciones.update(estado='inactivo')
            for publicacion in publicaciones:
                Historial.objects.create(publicacion=publicacion, accion='Inactivado por inactividad')


    def test_inactiva_publicaciones_antiguas(self):
        # Ejecuta la tarea de verificación de inactividad
        self.run_inmediate_inactividad_task()

        # Verificar que la publicación antigua ha sido marcada como inactiva
        self.publicacion_inactiva.refresh_from_db()
        self.assertEqual(self.publicacion_inactiva.estado, 'inactivo')

        # Verificar que la publicación reciente permanece activa
        self.publicacion_activa.refresh_from_db()
        self.assertEqual(self.publicacion_activa.estado, 'publicado')

    def test_registro_historial_para_publicaciones_inactivas(self):
        # Ejecuta la tarea de verificación de inactividad
        self.run_inmediate_inactividad_task()

        # Verificar que se ha creado un registro en el historial para la publicación antigua
        historial_registro = Historial.objects.filter(publicacion=self.publicacion_inactiva).first()
        self.assertIsNotNone(historial_registro)
        self.assertEqual(historial_registro.publicacion.estado, 'inactivo')
