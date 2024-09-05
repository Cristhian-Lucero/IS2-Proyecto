from django.urls import path
from .views import PerfilDetailView

urlpatterns = [
    path('', PerfilDetailView.as_view(), name='ver_perfil'),
]