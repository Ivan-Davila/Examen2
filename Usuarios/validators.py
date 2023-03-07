from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

def validar_contrasena(value):
    if len(value) < 10:
        raise ValidationError("La contraseña debe tener al menos 10 caracteres")
    if not re.match("^(?=.*[0-9])(?=.*[!@#$%^&*-_.])[a-zA-Z0-9!@#$%^&*]{10,}$", value):
        raise ValidationError("La contraseña solo debe contener números y caracteres especiales")
    
def validate_email_unique(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Este correo ya está registrado.')