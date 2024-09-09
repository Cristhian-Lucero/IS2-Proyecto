"""
Configuración WSGI para el proyecto IS2_Proyecto.

Expone el callable WSGI como una variable a nivel de módulo llamada ``application``.

Este archivo se usa para desplegar la aplicación en servidores WSGI.

Para más información, consulta:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""


import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/IS2-Proyecto')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IS2_Proyecto.settings')

application = get_wsgi_application()
