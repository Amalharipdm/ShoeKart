# Generated by Django 4.2.1 on 2023-06-21 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_detail', '0009_cartitemslist_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemslist',
            name='user_coupon_active',
            field=models.BooleanField(default=True),
        ),
    ]