from django import forms
from .models import Publicacion

from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['encabezado', 'cuerpo', 'imagen']

