# Generated by Django 4.1.6 on 2023-02-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='registra',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='user_type',
            field=models.CharField(choices=[('administrator', 'Administrator'), ('distribuidor', 'Distribuidor'), ('cliente', 'Cliente')], max_length=20),
        ),
    ]
