"""
Configuración de URLs para IS2_Proyecto.

Este archivo define las URLs y las vistas que las gestionarán. También incluye
las rutas de documentación de la API usando Swagger y Redoc.

Rutas disponibles:
- URLs de login y publicaciones.
- Panel de administración.
- Documentación de la API en Swagger UI.
- Documentación de la API en Redoc.

Para más información, consulta:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path             # documentacion
from rest_framework import permissions      #
from drf_yasg.views import get_schema_view  #
from drf_yasg import openapi                #

schema_view = get_schema_view(
   openapi.Info(
      title="CSM Docs",
      default_version='v1',
      description="Bienvenido a la documentación",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cristhianlucero1@fpuna.edu.py"),
      license=openapi.License(name="IS2 Grupo 7"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,), #para no hacer el login
)

urlpatterns = [
    path('', include('login.urls')),
    path('', include('publicacion.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), #documentacion
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),          #
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
