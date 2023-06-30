from django.contrib import admin
from .models import *

# Register your models here.


class CartItemsListAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity')

class MultipleAddressesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'address_line_1','address_line_2', 'area', 'state', 'is_default')

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'active'] 

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user', 'order_date', 'order_status', 'payment_status', 'payment_method', 'checkout_status', 'to_address', 'coupon')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'product', 'quantity')

admin.site.register(CartItemsList, CartItemsListAdmin)
admin.site.register(MultipleAddresses, MultipleAddressesAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Coupon, CouponAdmin)
