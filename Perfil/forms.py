from django import forms
from .models import *
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['logo', 'descripcion']  # Incluye el campo 'logo' para subir la imagen
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Extraemos el request de kwargs si está presente
        super(PerfilForm, self).__init__(*args, **kwargs)
        
        if request:
            usuario = Usuario.objects.get(user_id=request.user.id)
            self.fields['descripcion'].initial = usuario.descripcion  # Asigna el valor inicial
