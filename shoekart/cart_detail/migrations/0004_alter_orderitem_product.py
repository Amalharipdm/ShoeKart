# Generated by Django 4.2.1 on 2023-06-13 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_product_product_thumbnail'),
        ('cart_detail', '0003_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productvarient'),
        ),
    ]