from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TipoUsuario(models.Model):
    tipo_usuario=models.CharField(max_length=30)

class PerfilUsuario(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[
        ('administrator', 'Administrator'),
        ('distributor', 'Distributor'),
        ('cliente', 'Cliente'),
    ])
    creditos=models.PositiveIntegerField()
    registra=models.CharField(max_length=30)
