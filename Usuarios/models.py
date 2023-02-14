from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20)
    creditos=models.PositiveIntegerField()
    registra=models.CharField(max_length=30)
