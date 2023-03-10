# Generated by Django 4.1.6 on 2023-03-02 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Usuarios', '0004_alter_perfilusuario_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TipoUsuario',
        ),
        migrations.RenameField(
            model_name='perfilusuario',
            old_name='user',
            new_name='usuario',
        ),
        migrations.RemoveField(
            model_name='perfilusuario',
            name='registra',
        ),
        migrations.RemoveField(
            model_name='perfilusuario',
            name='user_type',
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='registrado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registrado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('A', 'Administrador'), ('D', 'Distribuidor'), ('C', 'Cliente')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='creditos',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
