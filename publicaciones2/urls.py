from django.urls import path
from . import views

urlpatterns = [
    path('crear-publicacion/', views.crear_publicacion, name='crear_publicacion'),
    path('crear-publicacion/<int:pk>/', views.crear_publicacion, name='editar_publicacion'),
    path('previsualizacion/<int:pk>/', views.previsualizacion, name='previsualizacion'),
    path('guardar-publicacion/<int:pk>/', views.guardar_publicacion, name='guardar_publicacion'),
    path('mis-publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('eliminar-publicacion/<int:pk>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('modificar-publicacion/<int:pk>/', views.modificar_publicacion, name='modificar_publicacion'),
]