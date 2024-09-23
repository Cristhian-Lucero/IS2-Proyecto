"""
URLs de la aplicación 'crearpublicaciones'.

Este archivo define las rutas de URL para gestionar las diferentes acciones
relacionadas con las publicaciones, como crear, modificar, eliminar, previsualizar,
y gestionar plantillas.
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('crear/<int:categoria_id>/', crear_publicacion, name='crear_publicacion'),
    path('previsualizar/<int:publicacion_id>/', previsualizar_publicacion, name='previsualizar_publicacion'),
    path('mis-publicaciones/', mis_publicaciones, name='mis_publicaciones'),
    path('modificar/<int:publicacion_id>/', modificar_publicacion, name='modificar_publicacion'),
    path('eliminar/<int:publicacion_id>/', eliminar_publicacion, name='eliminar_publicacion'),
    path('seleccionar-plantilla/<int:categoria_id>/', seleccionar_plantilla, name='seleccionar_plantilla'),
    path('personalizable/', personalizable, name='personalizable'),
    path('gestionPublicacionOtros/<int:categoria_id>/', gestionPublicacionOtros, name='gestionPublicacionOtros'),
    path('eliminar_publicacion_otros/<int:publicacion_id>/', eliminar_publicacion_otros, name='eliminar_publicacion_otros'),
]

