# Generated by Django 4.2.1 on 2023-05-28 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_product_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='colors',
        ),
        migrations.AddField(
            model_name='productimages',
            name='colors',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.productcolors'),
        ),
    ]
