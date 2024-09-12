from django.urls import include, path
from .views import *
from . import views

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('mis/', views.mis_publicaciones, name='mis_publicaciones'),
]

