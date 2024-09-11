from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'texto_corto', 'texto_largo', 'imagen1', 'imagen2']