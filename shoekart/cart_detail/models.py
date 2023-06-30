from accounts.models import *
from products.models import *
import uuid
from django.utils import timezone
from decimal import Decimal


# Create your models here.

class Coupon(models.Model):
    code        =   models.CharField(max_length=50, unique=True)
    discount    =   models.DecimalField(max_digits=5, decimal_places=2)
    valid_from  =   models.DateTimeField(default=timezone.now)
    valid_to    =   models.DateField()
    active      =   models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to
    
    def __str__(self):
        return self.code

    
class CartItemsList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    user_coupon_active = models.BooleanField(default=True)  

    def __str__(self):
        return str(self.product)
    
    def get_subtotal(self):
        return self.quantity * self.product.name.product_price
    
    

    def get_total(self):
        total = 0
        for cart_item in self:
            total += cart_item.get_subtotal()
        return total
    

    @staticmethod
    def get_total_discount(cart_items):
        total_discount = Decimal('0.0')
        for cart_item in cart_items:
            if cart_item.coupon:
                subtotal = cart_item.get_subtotal()
                discount = subtotal * (cart_item.coupon.discount / Decimal('100'))
                total_discount += discount
        return total_discount


        
    
    def get_total_payment_amount(user):
        total_payment_amount = Decimal('0.0')
        cart_items = CartItemsList.objects.filter(user=user)
        for item in cart_items:
            total_payment_amount += item.get_subtotal()
        if cart_items and cart_items[0].coupon:
            total_payment_amount -= CartItemsList.get_total_discount(cart_items)
        return total_payment_amount





    
class MultipleAddresses(models.Model):
    user                    = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name              = models.CharField(max_length=100, null=True, blank=True)
    last_name               = models.CharField(max_length=100, null=True, blank=True)
    phone_number            = models.CharField(max_length=50, null=True, blank=True)
    address_line_1          = models.CharField(max_length=100, null=True, blank=True)
    address_line_2          = models.CharField(max_length=100, null=True, blank=True)
    postcode                = models.CharField(max_length=10, null=True, blank=True)
    area                    = models.CharField(max_length=100, null=True, blank=True)
    state                   = models.CharField(max_length=100, null=True, blank=True)
    is_default              = models.BooleanField(default=False)



    def __str__(self):
        return self.first_name
    


    
    
 
class Orders(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
   )
    PAYMENT_METHOD = (
        ('COD', 'COD'),
        ('Razorpay', 'Razorpay')
    )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    CHECKOUT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    order_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    checkout_status = models.CharField(max_length=50,choices=CHECKOUT_STATUS)
    to_address = models.ForeignKey(MultipleAddresses, on_delete=models.CASCADE)
    total_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.email} - Order No: {str(self.order_no)}"
    
    def get_total(self):
        order_items = OrderItem.objects.filter(order_no=self)
        total = sum(item.get_subtotal() for item in order_items)
        return total
    
    def get_total_discount(self):
        if self.coupon:
            return self.get_total() * (self.coupon.discount / 100)
        return 0

    
    def get_total_payment_amount(self):
        if self.coupon:
            return self.get_total() - self.get_total_discount()
        return self.get_total()

    


class OrderItem(models.Model):
    order_no = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.order_no)
    
    def get_subtotal(self):
        return self.quantity * self.product.name.product_price

   