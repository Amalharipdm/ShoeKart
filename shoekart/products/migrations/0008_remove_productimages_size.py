# Generated by Django 4.2.1 on 2023-05-29 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productimages_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='size',
        ),
    ]
