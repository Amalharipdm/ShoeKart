# Generated by Django 4.2.1 on 2023-06-13 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0013_alter_product_product_thumbnail'),
        ('cart_detail', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Out for Shipping', 'Out for Shipping'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], max_length=50)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], max_length=50)),
                ('payment_method', models.CharField(choices=[('COD', 'COD'), ('Razorpay', 'Razorpay')], max_length=50)),
                ('checkout_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=50)),
                ('total_mrp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('coupon_discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('to_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart_detail.multipleaddresses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='OrderItems',
            new_name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart_detail.orders'),
        ),
    ]