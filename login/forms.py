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

class UpdateNombreApellido(forms.Form):

    box_nombre = forms.CharField(label="Nombre", max_length=150)
    box_apellido = forms.CharField(label="Apellido", max_length=150)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Guardamos el request en self.request
        super(UpdateNombreApellido, self).__init__(*args, **kwargs)
        
        if self.request:
            usuario = self.request.user
            self.fields['box_nombre'].initial = usuario.first_name  # Asigna el valor inicial
            self.fields['box_apellido'].initial = usuario.last_name  # Asigna el valor inicial
    
    def save(self):
        if self.request:
            usuario = self.request.user
            # Actualizamos el usuario con los valores del formulario
            usuario.first_name = self.cleaned_data['box_nombre']
            usuario.last_name = self.cleaned_data['box_apellido']
            usuario.save()  # Guardamos los cambios en el modelo User

class UpdateEmail(forms.Form):

    box_email_nuevo = forms.CharField(label="Email Nuevo", max_length=100)
    box_email_repetido = forms.CharField(label="Repetir Email", max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Guardamos el request en self.request
        super(UpdateEmail, self).__init__(*args, **kwargs)

    def clean(self):
        # Validamos que los dos emails coincidan
        cleaned_data = super().clean()
        email_nuevo = cleaned_data.get('box_email_nuevo')
        email_repetido = cleaned_data.get('box_email_repetido')

        if email_nuevo != email_repetido:
            raise forms.ValidationError("Los emails no coinciden.")

        return cleaned_data

    def save(self):
        if self.request:
            usuario = self.request.user

            # Solo guardamos el nuevo email si todo está validado
            usuario.email = self.cleaned_data['box_email_nuevo']
            usuario.save()  # Guardamos los cambios en el modelo User


class UpdatePassword(forms.Form):

    box_password_viejo = forms.CharField(label="Contraseña Antigua", max_length=100)
    box_password_nuevo = forms.CharField(label="Contraseña Nueva", max_length=100)
    box_password_repetido = forms.CharField(label="Repetir Nueva Repetida", max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Guardamos el request en self.request
        super(UpdatePassword, self).__init__(*args, **kwargs)

    def clean(self):
        # Validamos que los dos emails coincidan
        cleaned_data = super().clean()
        password_viejo = cleaned_data.get('box_password_viejo')
        password_nuevo = cleaned_data.get('box_password_nuevo')
        password_repetido = cleaned_data.get('box_password_repetido')
 
        if not self.request.user.check_password(password_viejo):
            raise forms.ValidationError("La contraseña vieja no coincide")

        if password_nuevo != password_repetido:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self):
        if self.request:
            usuario = self.request.user
            # Solo guardamos el nuevo email si todo está validado
            nuevo_password = self.cleaned_data['box_password_nuevo']
            usuario.set_password(nuevo_password)
            
            usuario.save()  # Guardamos los cambios en el modelo User

