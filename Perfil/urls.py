from django.urls import path
from .views import *

urlpatterns = [
    path('', PerfilDetailView.as_view(), name='ver_perfil'),
]
