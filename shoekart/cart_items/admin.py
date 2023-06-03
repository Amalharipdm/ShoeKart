from django.contrib import admin
from .models import *

# Register your models here.

class CartUserItemsAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity')

admin.site.register(CartUserItems, CartUserItemsAdmin)