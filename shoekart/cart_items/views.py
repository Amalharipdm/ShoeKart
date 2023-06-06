from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *

# Create your views here.


def cart_view(request):
    cart_items = CartUserItems.objects.filter(user=request.user)
    total_amount = CartUserItems.get_total(cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount
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
        return redirect('cart_view')
    else:
        return redirect('product_detail', id=id) 


def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartUserItems, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


def address_details(request):
    return render(request, 'cart_items/address_details.html')