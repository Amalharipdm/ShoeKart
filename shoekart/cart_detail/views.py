from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import razorpay
from shoekart.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import date
from django.db.models import Sum
from decimal import Decimal
import random


# Create your views here.


def cart_view(request, coupon_id=None):
    cart_items = CartItemsList.objects.filter(user=request.user)
    total_amount = CartItemsList.get_total(cart_items)
    applied_coupon_ids = CartItemsList.objects.filter(user=request.user, coupon__isnull=False).values_list('coupon', flat=True)
    coupons = Coupon.objects.filter(active=True, valid_from__lte=timezone.now(), valid_to__gte=date.today()).exclude(id__in=applied_coupon_ids)
    light_colors = ["rgb(255, 204, 204)", "rgb(204, 229, 255)", "rgb(224, 224, 255)"]
    for coupon in coupons:
        coupon.color = random.choice(light_colors)
    order = Orders.objects.first()
    discount_price = order.get_total_discount() if order else 0
    total_discount_amount = request.session.pop('total_discount_amount', 0)
    
    selected_coupon = None
    applied_coupon = None

    total_payment_amount = total_amount 

    

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'coupons': coupons,
        'discount_price': discount_price,
        'selected_coupon': None,
        'applied_coupon': None,
        'total_discount_amount' : total_discount_amount,
        'discount_amount': total_discount_amount,
        'total_payment_amount': total_amount,
    }
    
    coupon_id = request.GET.get('coupon')
    if coupon_id:
        selected_coupon = get_object_or_404(Coupon, id=coupon_id)
        context['selected_coupon'] = selected_coupon

        discount_amount = selected_coupon.discount * total_amount / 100
        context['discount_amount'] = discount_amount

    applied_coupon_id = request.session.get('applied_coupon')
    if applied_coupon_id:
        applied_coupon = get_object_or_404(Coupon, id=applied_coupon_id)
        context['applied_coupon'] = applied_coupon

        total_discount_amount = applied_coupon.discount * total_amount / 100
        context['total_discount_amount'] = total_discount_amount

        total_payment_amount = total_amount - total_discount_amount
        context['total_payment_amount'] = total_payment_amount
   
    if total_discount_amount == 0 or applied_coupon_id is None:
        context['total_payment_amount'] = total_amount
        context['applied_coupon'] = None

        print(total_payment_amount)

    if 'remove_coupon' in request.POST:
        remove_coupon_id = request.POST.get('remove_coupon')
        if remove_coupon_id:
            remove_coupon = get_object_or_404(Coupon, id=remove_coupon_id)
            if remove_coupon == applied_coupon:
                request.session.pop('applied_coupon', None)
                context['applied_coupon'] = None
                context['total_discount_amount'] = 0
                context['total_payment_amount'] = total_amount

    return render(request, 'cart_items/cart_home.html', context)




def apply_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id) 
    cart_items = CartItemsList.objects.filter(user=request.user)  
    if cart_items.exists():
        for cart_item in cart_items:
            cart_item.coupon = coupon
            cart_item.user_coupon_active = False
            cart_item.save()
        
        total_discount_amount = cart_items.aggregate(total_discount=Sum('coupon__discount'))['total_discount']        
        total_discount_amount = round(total_discount_amount, 2) if total_discount_amount else Decimal('0')
        request.session['total_discount_amount'] = float(total_discount_amount)
        request.session['applied_coupon'] = coupon.id
      
        messages.success(request, 'Coupon applied successfully.')
        
    else:
        messages.error(request, 'Failed to apply the coupon.')
    return redirect('cart_view')

def remove_coupon_view(request):
    if request.method == 'POST':
        remove_coupon_id = request.POST.get('remove_coupon')
        if remove_coupon_id:
            remove_coupon = get_object_or_404(Coupon, id=remove_coupon_id)
            if remove_coupon == request.session.get('applied_coupon'):
                request.session.pop('applied_coupon')
                # Optionally, you can update any other relevant session data or perform additional actions
    return redirect('cart_view')




def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItemsList, id=item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        product_varient = get_object_or_404(ProductVarient, id=cart_item.product.id)
        available_stock = product_varient.stock
        if action == 'increment':
            if cart_item.quantity < available_stock:
                cart_item.quantity += 1
            else:
                messages.warning(request, "The stock quantity is insufficient.")
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1        
        cart_item.save()
        return redirect('cart_view')  
    return render(request, 'update_cart_item.html', {'cart_item': cart_item})




# def update_cart_item(request):
#     if request.method == 'POST':
#         cart_item_id = int(request.POST.get('id'))
#         print(cart_item_id,111111111111)
#         cart_item_quantity = int(request.POST.get('quantity'))

#         cart_item = CartItemsList.objects.get(id=cart_item_id)
#         cart_item.quantity = cart_item_quantity
#         cart_item.save()

#         return HttpResponse('OK')




def add_to_cart(request, id):
    if request.method == 'POST':
        varient_id = request.POST.get('id')
        product_varient = ProductVarient.objects.get(id=varient_id)
        product_cart_item = CartItemsList.objects.filter(user=request.user, product=product_varient)
        cart_items = None
        if len(product_cart_item) == 0:
            cart_items = CartItemsList.objects.create(user=request.user,product=product_varient)
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
    cart_item = get_object_or_404(CartItemsList, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

def address_home(request):
    return render(request, 'cart_items/checkout.html')


# cart_detail.html views

def display_addresses(request):
    addresses = MultipleAddresses.objects.filter(user=request.user)
    cart_items = CartItemsList.objects.filter(user=request.user)
    total_amount = CartItemsList.get_total(cart_items)
    discount_amount = CartItemsList.get_total_discount(cart_items)
    total_mrp = 0.0
    for item in cart_items:
        product_varient = get_object_or_404(ProductVarient, id=item.product.id)
        if item.quantity > product_varient.stock:
            messages.warning(request, f"The stock quantity is insufficient for {product_varient.name}.Please adjust your cart.")
            return redirect('cart_view')
        total_mrp += item.product.name.product_price * item.quantity
        product_varient.stock -= item.quantity
        product_varient.save()
    total_mrp=Decimal(total_mrp)
    total_payment_amount = CartItemsList.get_total_payment_amount(request.user)
    selected_address_id = request.session.get('selected_address')
    selected_address = None
    if selected_address_id:
        selected_address = get_object_or_404(MultipleAddresses, id=selected_address_id)
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'discount_amount': discount_amount,
        'total_payment_amount': total_payment_amount,
        'addresses': addresses,
        'selected_address': selected_address,
    }
    if request.method=='POST':
        address_id = request.session.get('selected_address')
        address = get_object_or_404(MultipleAddresses, id=address_id)    
        order = Orders.objects.create(
            user=request.user,
            order_status='Pending',
            payment_status='Completed',
            payment_method='Razorpay',
            checkout_status='Completed',
            to_address=address,
            total_mrp=total_mrp,  
            discount_amount=discount_amount,   
            payment_amount=total_mrp-discount_amount
        )
        cart_items = CartItemsList.objects.filter(user=request.user)
        
        for item in cart_items:
            OrderItem.objects.create(
                order_no=order,
                product=item.product,
                quantity=item.quantity
            )
        del request.session['selected_address']
        cart_items.delete()
        return order_detail(request,order.id)
    return render(request, 'cart_items/checkout.html', context)

def add_address(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        postcode = request.POST.get('postcode')
        area = request.POST.get('area')
        state = request.POST.get('state')
        
        address = MultipleAddresses.objects.create(
            user = user,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            address_line_1 = address_line_1,
            address_line_2 = address_line_2,
            postcode = postcode,
            area = area,
            state = state
        )
        address.save()
        return redirect('display_addresses')
    return render(request, 'cart_items/checkout.html')

def address_edit(request):
    addresses = MultipleAddresses.objects.all()
    context = {'addresses':addresses}
    return redirect('display_addresses',context)

def address_update(request,id):
    address = get_object_or_404(MultipleAddresses, id=id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        postcode = request.POST.get('postcode')
        area = request.POST.get('area')
        state = request.POST.get('state')

        address.first_name=first_name
        address.last_name=last_name
        address.phone_number=phone_number
        address.address_line_1=address_line_1
        address.address_line_2=address_line_2
        address.postcode=postcode
        address.area=area
        address.state=state

        address.save()
        return redirect('display_addresses')
    return render(redirect, 'cart_items/checkout.html', {'address': address})
        
def address_delete(request,id):
    addresses = MultipleAddresses.objects.get(id=id)
    addresses.delete()
    context = {'addresses':addresses}
    return redirect('display_addresses')

def use_address(request, address_id):
    address = get_object_or_404(MultipleAddresses, id=address_id)
    request.session['selected_address'] = address.id
    return redirect('display_addresses')

@transaction.atomic
def place_order(request):
    address_id = request.session.get('selected_address')
    if address_id is None:
        messages.error(request, 'Please select an address before placing the order.')
        return redirect('display_addresses') 
    address = get_object_or_404(MultipleAddresses, id=address_id)    
    
    cart_items = CartItemsList.objects.filter(user=request.user)
    total_discount = CartItemsList.get_total_discount(cart_items)
    total_mrp = 0.0
    # total_discount = 0.0 
    
    for item in cart_items:
        product_varient = get_object_or_404(ProductVarient, id=item.product.id)
        if item.quantity > product_varient.stock:
            messages.warning(request, f"The stock quantity is insufficient for {product_varient.name}.Please adjust your cart.")
            return redirect('cart_view')
        total_mrp += item.product.name.product_price * item.quantity
        product_varient.stock -= item.quantity
        product_varient.save()
    
    total_mrp=Decimal(total_mrp)
    print('payment_amount:',total_mrp-total_discount)
    order = Orders.objects.create(
        user=request.user,
        order_status='Pending',
        payment_status='Pending',
        payment_method='COD',
        checkout_status='Pending',
        to_address=address,
        total_mrp=total_mrp,  
        coupon=None,
        discount_amount=total_discount,  
        payment_amount=total_mrp - total_discount 
    )
    if 'applied_coupon' in request.session:
        coupon_code = request.session['applied_coupon']
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if coupon:
            order.coupon = coupon  
            order.payment_amount -= coupon.discount 
            order.save()
        del request.session['applied_coupon']
    cart_items = CartItemsList.objects.filter(user=request.user)
    
    for item in cart_items:
        OrderItem.objects.create(
            order_no=order,
            product=item.product,
            quantity=item.quantity
        )
    del request.session['selected_address']
    cart_items.delete()
    return order_detail(request,order.id)






# ------------------------------------------------------

def order_detail(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    cart_items = CartItemsList.objects.filter(user=order.user)
    total_discount = CartItemsList.get_total_discount(cart_items)
    total_payment_amount = CartItemsList.get_total_payment_amount(order.user)
    context = {
        'order': order,
        'total_discount':total_discount,
        'total_payment_amount':total_payment_amount,
    }
    return render(request, 'cart_items/order_detail.html', context)
    
       

def razorpay_payment(request):
    if request.method == "POST":
        amount = int(request.POST.get('amount')) * 100  # Amount in paise
        name = request.POST.get('name')
        email = request.POST.get('email')
        client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'receipt_order_001',
            'notes': {
                'name': name,
                'email': email,
            },
        }
        payment = client.order.create(data=payment_data)
        return render(request, 'checkout.html', {'payment': payment})
    return render(request, 'payment.html')




