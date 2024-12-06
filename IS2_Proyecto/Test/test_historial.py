from django.test import TestCase, RequestFactory
from login.models import Categoria, Rol
from crearpublicaciones.models import Publicacion, Historial
from django.contrib.auth.models import User
from datetime import datetime
from crearpublicaciones.views import historial_publicacion, guardar_publicacion_ajax, personalizable
from Tablero.views import update_task_state

import json

class HistorialPublicacionViewTestCase(TestCase):
    fixtures = [
        'IS2_Proyecto/Test/fixtures/roles_fixture.json',
        'IS2_Proyecto/Test/fixtures/permisos_fixture.json',
        'IS2_Proyecto/Test/fixtures/categorias_fixture.json',
        'IS2_Proyecto/Test/fixtures/users_fixture.json'
    ]

    def setUp(self):
        # Crear un usuario y publicaciones de prueba
        self.factory = RequestFactory()
        self.user = User.objects.get(username='superuser')
        self.categoria = Categoria.objects.get(id=1)

        # Crear publicación inicial
        self.publicacion = Publicacion.objects.create(
            titulo='Título Inicial',
            contenido_html='<p>Contenido inicial de la publicación.</p>',
            estado='borrador',
            categoria=self.categoria,
            user=self.user
        )

        # Crear un historial inicial para la publicación
        self.historial = Historial.objects.create(
            publicacion=self.publicacion,
            usuario=self.user,
            accion='creado'
        )

    def test_crear_historial_al_modificar_titulo_cuerpo(self):
       # Probar que modificar el título y el contenido crea un historial
        request = self.factory.post(
            f'/guardar_publicacion_ajax/{self.publicacion.id}/',
            data={
                'title': 'Título Modificado',
                'content': '<p>Contenido modificado de la publicación.</p>'
            },
            content_type='application/json'
        )
        request.user = self.user

        response = guardar_publicacion_ajax(request, publicacion_id=self.publicacion.id)
        self.assertEqual(response.status_code, 200)

        # Verificar que se creó un nuevo registro en el historial
        historial_reciente = Historial.objects.filter(publicacion=self.publicacion).latest('fecha_evento')
        self.assertEqual(historial_reciente.accion, 'modificado_titulo_cuerpo')

    def test_crear_historial_al_modificar_titulo(self):
        #Probar que modificar solo el título crea un historial
        
        request = self.factory.post(
            f'/guardar_publicacion_ajax/{self.publicacion.id}/',
            data={
                'title': 'Título Modificado',
                'content': '<p>Contenido inicial de la publicación.</p>'
            },
            content_type='application/json'
        )
        request.user = self.user

        response = guardar_publicacion_ajax(request, publicacion_id=self.publicacion.id)
        self.assertEqual(response.status_code, 200)

        # Verificar que se creó un nuevo registro en el historial
        historial_reciente = Historial.objects.filter(publicacion=self.publicacion).latest('fecha_evento')
        self.assertEqual(historial_reciente.accion, 'modificado_titulo')

    def test_crear_historial_al_modificar_cuerpo(self):
        #Probar que modificar solo el título crea un historial
        request = self.factory.post(
            f'/guardar_publicacion_ajax/{self.publicacion.id}/',
            data={
                'title': 'Título Inicial',
                'content': '<p>Contenido modificado de la publicación.</p>'
            },
            content_type='application/json'
        )
        request.user = self.user

        response = guardar_publicacion_ajax(request, publicacion_id=self.publicacion.id)
        self.assertEqual(response.status_code, 200)

        # Verificar que se creó un nuevo registro en el historial
        historial_reciente = Historial.objects.filter(publicacion=self.publicacion).latest('fecha_evento')
        self.assertEqual(historial_reciente.accion, 'modificado_cuerpo')
    
    def test_cambio_estado(self):
        #Probar que el estado de la publicación cambia correctamente y se registra en el historial

        #solicitud POST para cambiar el estado
        new_state = "revision"
        request = self.factory.post(
            f'/update-task-state/{self.publicacion.id}/',
            data=json.dumps({'estado': new_state}),
            content_type='application/json'
        )
        request.user = self.user

        response = update_task_state(request, task_id=self.publicacion.id)

        # Verificar respuesta
        self.assertEqual(response.status_code, 200)

        # Verificar que el estado de la publicación ha cambiado
        self.publicacion.refresh_from_db()
        self.assertEqual(self.publicacion.estado, new_state)

        # Verificar que se ha creado un registro en el historial
        historial = Historial.objects.filter(publicacion=self.publicacion).latest('fecha_evento')
        self.assertEqual(historial.accion, "cambio_estado")
        self.assertEqual(historial.estado_anterior, "borrador")
        self.assertEqual(historial.estado_nuevo, "revision")
    
    def test_crear_y_guardar_publicacion(self):
        #Probar el flujo de creación y guardado de una publicación"""

        # solicitud a la vista 'personalizable'
        request = self.factory.get(f'/personalizable/{self.categoria.id}/')
        request.user = self.user
        response = personalizable(request, categoria_id=self.categoria.id)

        self.assertEqual(response.status_code, 200)

        # Crear una publicación inicial
        publicacion = Publicacion.objects.create(
            titulo='',
            contenido_html='',
            estado='borrador',
            categoria=self.categoria,
            user=self.user
        )

        # Verificar que la publicación inicial se haya creado correctamente
        self.assertEqual(publicacion.titulo, '')
        self.assertEqual(publicacion.contenido_html, '')
        self.assertEqual(publicacion.estado, 'borrador')

        # guardar el título y el contenido
        nuevo_titulo = "Título de Prueba"
        nuevo_contenido = "<h2>Encabezado</h2><p>Contenido detallado.</p>"

        request = self.factory.post(
            f'/guardar_publicacion_ajax/{publicacion.id}/',
            data=json.dumps({
                "title": nuevo_titulo,
                "content": nuevo_contenido
            }),
            content_type='application/json'
        )
        request.user = self.user

        # procesar la solicitud
        response = guardar_publicacion_ajax(request, publicacion_id=publicacion.id)

        # Verificar que la publicación se haya guardado correctamente
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["status"], "success")

        # verificar los cambios
        publicacion.refresh_from_db()
        self.assertEqual(publicacion.titulo, nuevo_titulo)
        self.assertEqual(publicacion.contenido_html, nuevo_contenido)

        # verificar que se haya registrado un historial
        historial = Historial.objects.filter(publicacion=publicacion).latest('fecha_evento')
        self.assertEqual(historial.accion, "creado")