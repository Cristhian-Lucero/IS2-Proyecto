from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('modificar/<int:pk>/', views.modificar_publicacion, name='modificar_publicacion'),
    path('eliminar/<int:pk>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('previsualizacion/<int:pk>/', views.previsualizacion, name='previsualizacion'),
    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
]
