from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.
class PerfilUsuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('A', 'Administrador'),
        ('D', 'Distribuidor'),
        ('C', 'Cliente'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=1, choices=TIPO_USUARIO_CHOICES)
    creditos = models.IntegerField(null=True, blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrado_por', blank=True, null=True)
    class Meta:
        permissions = [
            ('can_view_users_list', 'Can view users list'),
            ('cambiar_credito', 'Cambiar credito de cliente')
        ]