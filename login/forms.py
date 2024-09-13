"""
Formularios para gestionar categorías y roles en la aplicación login.

Incluye formularios personalizados para la creación y edición de Categoría y Rol,
con validación y selección de permisos.
"""


from django import forms
from .models import *

class CreateNewCategoria(forms.Form):
    """
    Formulario para crear una nueva categoría.

    Campos:
        box_descripcion_corta (CharField): Campo para ingresar la descripción corta de la categoría. Máximo 100 caracteres.
        box_descripcion_larga (CharField): Campo de texto para ingresar una descripción detallada de la categoría.
        box_estado (ChoiceField): Campo para seleccionar el estado de la categoría ('Activo' o 'Inactivo').
    """

    box_descripcion_corta = forms.CharField(label="Descripcion Corta", max_length=100)
    box_descripcion_larga = forms.CharField(label="Descripcion Larga", widget=forms.Textarea)
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    box_estado = forms.ChoiceField(label="Estado", choices=ESTADO_CHOICES)

class CreateNewRol(forms.Form):
    """
    Formulario para crear un nuevo rol.

    Campos:
        box_nombre (CharField): Campo para ingresar el nombre del rol. Máximo 100 caracteres.
        box_descripcion (CharField): Campo de texto para ingresar una descripción detallada del rol.
        permisos (MultipleChoiceField): Campo para seleccionar múltiples permisos asociados al rol.
    """
    
    box_nombre= forms.CharField(label="Nombre", max_length=100)
    box_descripcion = forms.CharField(
        label="Descripcion", 
        widget=forms.Textarea (attrs={'rows': 5, 'cols': 50, 'style': 'width:100%;'}))

    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario de creación de roles.

        Configura el campo 'permisos' con las opciones disponibles en el modelo Permiso,
        permitiendo al usuario seleccionar múltiples permisos para el rol.
        """

        super(CreateNewRol, self).__init__(*args, **kwargs)
        permisos_choices = [(permiso.id, permiso.nombre) for permiso in Permiso.objects.all()]
        self.fields['permisos'] = forms.MultipleChoiceField(
            label="Permisos",
            choices=permisos_choices,
            widget=forms.CheckboxSelectMultiple
        )

