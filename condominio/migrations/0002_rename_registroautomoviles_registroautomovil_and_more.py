# Generated by Django 5.1.4 on 2024-12-06 21:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RegistroAutomoviles',
            new_name='RegistroAutomovil',
        ),
        migrations.RenameModel(
            old_name='RegistroMascotas',
            new_name='RegistroMascota',
        ),
        migrations.RenameModel(
            old_name='RegistroReportes',
            new_name='RegistroReporte',
        ),
        migrations.RenameModel(
            old_name='RegistroVisitas',
            new_name='RegistroVisita',
        ),
    ]
