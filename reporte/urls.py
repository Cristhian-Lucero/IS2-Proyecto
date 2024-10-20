from django.urls import path
from .views import *

urlpatterns = [
    path('masVistos', masVistos, name='masVistos'),
    path('masLikeados', masLikeados, name='masLikeados'),
    path('listaReportes', listaReportes, name='listaReportes'),
    path('visualizarReporte/<int:reporte_id>', visualizarReporte, name='visualizarReporte'),
    path('eliminarReporte/<int:reporte_id>', eliminarReporte, name='eliminarReporte'),
]