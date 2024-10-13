from django import forms
from .models import *

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['logo', 'descripcion']  # Incluye el campo 'logo' para subir la imagen
