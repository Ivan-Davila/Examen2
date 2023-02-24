from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.

class TipoUsuario(models.Model):
    tipo_usuario=models.CharField(max_length=30)

class PerfilUsuario(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[
        ('administrator', 'Administrator'),
        ('distribuidor', 'Distribuidor'),
        ('cliente', 'Cliente'),
    ])
    creditos=models.PositiveIntegerField()
    registra=models.IntegerField()
    class Meta:
        permissions = [
            ('can_view_users_list', 'Can view users list'),
            ('cambiar_credito', 'Cambiar credito de cliente')
        ]