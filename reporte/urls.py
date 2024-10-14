from django.urls import path
from .views import *

urlpatterns = [
    path('masVistos', masVistos, name='masVistos'),
]