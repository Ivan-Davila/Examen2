from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PerfilUsuario
from django.contrib.auth.models import User
from .validators import validar_contrasena, validate_email_unique

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistroUsuarioForm(UserCreationForm):
    creditos = forms.IntegerField(required=False, initial=0)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), validators=[validar_contrasena])
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name','last_name')
    
    def save(self, request, tipo_usuario, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil_usuario = PerfilUsuario(usuario=user, tipo_usuario=tipo_usuario, creditos=self.cleaned_data.get('creditos'), registrado_por=request.user)
            perfil_usuario.save()
        return user

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email_unique(email)
        return email

class perfilForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
        }

    creditos = forms.IntegerField(disabled=True, label='Créditos')
    username = forms.CharField(disabled=True, label='Nombre de usuario')

    def __init__(self, *args, **kwargs):
        super(perfilForm, self).__init__(*args, **kwargs)
        self.fields['creditos'].initial = self.instance.perfilusuario.creditos
        self.fields['username'].initial = self.instance.username
        self.fields['password'].widget = forms.HiddenInput()
