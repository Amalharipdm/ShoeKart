# Generated by Django 4.2.1 on 2023-06-13 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart_detail', '0002_orders_rename_orderitems_orderitem_delete_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart_detail.cartitemslist'),
        ),
    ]