from django.urls import path
from .views import crear_publicacion, previsualizar_publicacion, mis_publicaciones, modificar_publicacion, eliminar_publicacion, seleccionar_plantilla, personalizable


urlpatterns = [
    path('crear/', crear_publicacion, name='crear_publicacion'),
    path('previsualizar/<int:pk>/', previsualizar_publicacion, name='previsualizar_publicacion'),
    path('mis-publicaciones/', mis_publicaciones, name='mis_publicaciones'),
    path('modificar/<int:pk>/', modificar_publicacion, name='modificar_publicacion'),
    path('eliminar/<int:pk>/', eliminar_publicacion, name='eliminar_publicacion'),
    path('seleccionar-plantilla/', seleccionar_plantilla, name='seleccionar_plantilla'),
    path('personalizable/', personalizable, name='personalizable'),
]

