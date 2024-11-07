from django.test import TestCase
from django.urls import reverse
from reporte.models import Reporte
from django.contrib.auth.models import User
from datetime import datetime

class ReporteTestCase(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json' 
    ]

    def setUp(self):
        # Crear un usuario y reportes de prueba
        self.usuario = User.objects.get(username='superuser')
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

    def test_mas_vistos(self):
        url = reverse('masVistos')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_mas_likeados(self):
        url = reverse('masLikeados')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_por_tiempo(self):
        url = reverse('porTiempo')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_publicado_por_tiempo(self):
        url = reverse('publicadoPorTiempo')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_promedio_revision(self):
        url = reverse('promedioRevision')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_lista_reportes(self):
        url = reverse('listaReportes')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_visualizacion_reporte(self):
        url = reverse('visualizarReporte', args=[self.reporte1.id])
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_eliminacion_reporte(self):
        url = reverse('eliminarReporte', args=[self.reporte1.id])
        self.client.login(username='superuser', password='superuser')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reporte.objects.count(), 1)

    def test_dashboard(self):
        url = reverse('dashboard')
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
