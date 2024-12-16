# Generated by Django 5.1.4 on 2024-12-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_codigo_blog_alter_blog_titulo_blog_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='fecha_modificado',
        ),
        migrations.AddField(
            model_name='blog',
            name='slug_blog',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='caracteristica_blog',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='titulo_blog',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
