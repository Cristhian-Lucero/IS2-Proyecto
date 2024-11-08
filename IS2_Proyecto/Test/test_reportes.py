from django.test import TestCase, RequestFactory
from Perfil.models import Usuario
from login.models import Categoria, Rol, UsuarioRolCategoria
from reporte.models import Reporte
from django.contrib.auth.models import User
from datetime import datetime
from reporte.views import *

class ReporteViewTestCase(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]

    def setUp(self):
        # Crear un usuario y reportes de prueba
        self.usuario = User.objects.get(username='superuser')
        self.factory = RequestFactory()
        self.categoria = Categoria.objects.get(id=1)
        self.rol_suscriptor = Rol.objects.get(id=5)
        self.rol_admin = Rol.objects.get(id=1)
        self.usuario_rol_categoria = UsuarioRolCategoria.objects.get(
            usuario=Usuario.objects.get(user_id=self.usuario),
            categoria=self.categoria,
            rol = self.rol_suscriptor  # Establecer el rol predeterminado como Suscriptor
        )
        self.usuario_rol_categoria.rol = self.rol_admin
        self.usuario_rol_categoria.save()
        
        self.reporte1 = Reporte.objects.create(
            titulo=f'Mas leido - {datetime.now().strftime("%Y-%m-%d")}',
            html_content='<p>Contenido de prueba para reporte mas leido</p>',
            fecha_creacion=datetime.now(),
            user=self.usuario.username,
            tipo='mas leido'
        )
        self.reporte2 = Reporte.objects.create(
            titulo=f'Mas likeado - {datetime.now().strftime("%Y-%m-%d")}',
            html_content='<p>Contenido de prueba para reporte mas likeado</p>',
            fecha_creacion=datetime.now(),
            user=self.usuario.username,
            tipo='mas likeado'
        )

    def test_mas_vistos_view(self):
        request = self.factory.get('/masVistos')
        request.user = self.usuario
        response = masVistos(request)
        self.assertEqual(response.status_code, 200)

    def test_mas_likeados_view(self):
        request = self.factory.get('/masLikeados')
        request.user = self.usuario
        response = masLikeados(request)
        self.assertEqual(response.status_code, 200)

    def test_por_tiempo_view(self):
        request = self.factory.get('/porTiempo')
        request.user = self.usuario
        response = porTiempo(request)
        self.assertEqual(response.status_code, 200)

    def test_publicado_por_tiempo_view(self):
        request = self.factory.get('/publicadoPorTiempo')
        request.user = self.usuario
        response = publicadoPorTiempo(request)
        self.assertEqual(response.status_code, 200)

    def test_promedio_revision_view(self):
        request = self.factory.get('/promedioRevision')
        request.user = self.usuario
        response = promedioRevision(request)
        self.assertEqual(response.status_code, 200)

    def test_lista_reportes_view(self):
        request = self.factory.get('/listaReportes')
        request.user = self.usuario
        response = listaReportes(request)
        self.assertEqual(response.status_code, 200)

    def test_visualizacion_reporte_view(self):
        request = self.factory.get(f'/visualizarReporte/{self.reporte1.id}')
        request.user = self.usuario
        response = visualizarReporte(request, reporte_id=self.reporte1.id)
        self.assertEqual(response.status_code, 200)

    def test_eliminacion_reporte_view(self):
        request = self.factory.post(f'/eliminarReporte/{self.reporte1.id}')
        request.user = self.usuario
        response = eliminarReporte(request, reporte_id=self.reporte1.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reporte.objects.count(), 1)

    def test_dashboard_view(self):
        request = self.factory.get('/dashboard')
        request.user = self.usuario
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)


    def test_inactivosPorFecha_view(self):
        request = self.factory.get('/inactivosPorFecha')
        request.user = self.usuario
        response = inactivosPorFecha(request)
        self.assertEqual(response.status_code, 200)