from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *

# Create your views here.


def cart_view(request):
    cart_items = CartUserItems.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart_items/cart_home.html', context)


def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = int(request.POST.get('id'))
        cart_item_quantity = int(request.POST.get('quantity'))

        cart_item = CartUserItems.objects.get(id=cart_item_id)
        cart_item.quantity = cart_item_quantity
        cart_item.save()

        return HttpResponse('OK')



def add_to_cart(request, id):
    if request.method == 'POST':
        varient_id = request.POST.get('id')
        product_varient = ProductVarient.objects.get(id=varient_id)
        product_cart_item = CartUserItems.objects.filter(user=request.user, product=product_varient)
        cart_items = None
        if len(product_cart_item) == 0:
            cart_items = CartUserItems.objects.create(user=request.user,product=product_varient)
            print('cart_items_quantity:',cart_items)
        else:
            cart_items = product_cart_item.first()
            cart_items.quantity += 1
            cart_items.save()
            print('cart_items_quantity:', cart_items.quantity)

        # cart_items.product_price = cart_items.quantity * cart_items.product.name.product_price
        # cart_items.save()
       
        return redirect('cart_view')
    else:
        return redirect('product_detail', id=id) 


     # quantity = request.POST.get('quantity')
        # variant = ProductVarient.objects.get(id=variant_id)
        # user = request.user
        # cart_item = CartUserItems.objects.filter(user=user, product=variant).first()
        # if cart_item:
        #     cart_item.quantity += int(quantity)
        #     cart_item.save()
        # else:
        #     cart_item = CartUserItems(user=user, product=variant, quantity=quantity)
        #     cart_item.save() 
