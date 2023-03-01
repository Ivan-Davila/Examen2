from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistroClienteForm(AuthenticationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        validators=[
            RegexValidator(
                regex=r'^[\d\W]+$',
                message='La contraseña debe contener solo números y caracteres especiales',
            ),
            MinLengthValidator(
                limit_value=10,
                message='La contraseña debe tener al menos 10 caracteres',
            ),
        ],
    )
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingresa una dirección de correo válida.')
    credito = forms.IntegerField(initial=0, label="Credito")
    
    class Meta:
        model = User
        fields =('username','email','first_name','last_name','password','user_type','credito')

