# Generated by Django 4.2.1 on 2023-05-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productvarient'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrands',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategories',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]