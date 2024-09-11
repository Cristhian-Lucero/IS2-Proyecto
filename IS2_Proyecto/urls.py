"""
URL configuration for IS2_Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
    path('perfil/', include('Perfil.urls')),
    path('publicacion/', include('publicacion.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('publicacion/', include('publicacion.urls')),  # Incluye las URLs de publicaciones
    path('accounts/', include('allauth.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), #documentacion
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),          #
    path('publicaciones/', include('crearpublicaciones.urls')),
    path('crearpublicaciones/', include('crearpublicaciones.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Agregar configuración para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

