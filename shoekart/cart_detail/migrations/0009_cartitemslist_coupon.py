# Generated by Django 4.2.1 on 2023-06-20 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart_detail', '0008_coupon_remove_orders_coupon_discount_orders_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemslist',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart_detail.coupon'),
        ),
    ]
