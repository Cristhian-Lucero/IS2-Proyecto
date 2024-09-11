from django.urls import include, path
from .views import *
from . import views

urlpatterns = [
    path('home/', home, name='home'),
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('mis/', views.mis_publicaciones, name='mis_publicaciones'),
]

