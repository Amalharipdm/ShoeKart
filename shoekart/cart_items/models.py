from accounts.models import *
from products.models import *

# Create your models here.

    

class CartUserItems(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.product)
    
    def get_subtotal(self):
        return self.quantity * self.product.name.product_price
    
    # @staticmethod
    # def get_total(user):
    #     cart_items = CartUserItems.objects.filter(user=user)
    #     total = sum(item.get_subtotal() for item in cart_items)
    #     return total

    @staticmethod
    def get_total(cart_items):
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_subtotal()
        return total
