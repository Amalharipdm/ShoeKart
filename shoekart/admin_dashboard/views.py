from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate, logout
from products.models import *
from accounts.models import *
from cart_detail.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import date,timedelta
from django.db.models import Sum
from decimal import Decimal
from datetime import date, timedelta
from django.db.models import Q


# Create your views here.




def admin_login(request):
    if 'admin_email' in request.session:
        return redirect('admin_home')
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user.is_admin:
           login(request,user)
           request.session['admin_email']=email
           return redirect('admin_home')
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')

    return render(request,"admin/admin_login.html")

def admin_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_login')


from datetime import datetime
@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
    current_month = 6  # Set the desired month (June: 6)
    current_year = date.today().year
    current_date = date.today()


    # Filter the orders for the current date and status as 'Completed'
    completed_orders_count = Orders.objects.filter(order_date__date=current_date, order_status='Pending').count()

    current_month_order = date.today().month


    # Filter the orders for the specified month and year
    orders = Orders.objects.filter(order_date__month=current_month, order_date__year=current_year)
    orders_monthly = Orders.objects.filter(order_date__month=current_month, order_date__year=current_year)
    completed_montly_orders_count = orders_monthly.filter(order_status='Pending').count()
   
   #Daily Revenue
    completed_orders = Orders.objects.filter(order_date__date=current_date, order_status='Pending')
    daily_total_payment_amount = completed_orders.aggregate(total_payment=Sum('payment_amount'))['total_payment']

    #Monthly Revenue
    completed_orders_montly = Orders.objects.filter(order_date__month=current_month_order, order_date__year=current_year, order_status='Pending')
    monthly_total_payment_amount = completed_orders_montly.aggregate(total_payment=Sum('payment_amount'))['total_payment']
   
   # Get the distinct brands from the ProductBrands model
    brands = ProductBrands.objects.all()

    # Dictionary to store the total_mrp for each brand
    brand_totals = {}

    # Calculate the total_mrp for each brand
    for brand in brands:
        product_variants = ProductVarient.objects.filter(name__product_brand=brand)
        total_mrp = orders.filter(orderitem__product__in=product_variants).aggregate(total_sales=Sum('total_mrp'))
        brand_totals[brand.brand_name] = total_mrp['total_sales'] if total_mrp['total_sales'] else 0

    context = {
        'brand_totals': brand_totals,
        'completed_orders_count': completed_orders_count,
        'completed_montly_orders_count': completed_montly_orders_count,
        'daily_total_payment_amount': daily_total_payment_amount,
        'monthly_total_payment_amount': monthly_total_payment_amount
    }

    return render(request, "admin/admin_home.html", context)



   





# user details

def user_home(request):
    user = Account.objects.all()
    user = Account.objects.exclude(is_admin=True).order_by('id')
    return render(request,'admin/user_home.html',{'users':user})




def user_edit(request,id):
    user = Account.objects.get(id=id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']     
        user = Account.objects.filter(id=id).update(first_name=first_name, last_name=last_name, email=email, username=username)
        return redirect('user_home')
    return render(request, 'admin/user_edit.html',{'user':user})

def block_user(request, id):
    if request.method == 'POST':
        user = Account.objects.get(pk=id)
        user.is_active = False
        user.save()
        return redirect('user_home')  

def unblock_user(request, id):
    if request.method == 'POST':
        user = Account.objects.get(pk=id)
        user.is_active = True
        user.save()
        return redirect('user_home') 

def user_search(request):
    # if 'admin' in request.session:
    if request.method == 'GET':
        user_search = request.GET.get('user_search')
        user = Account.objects.filter(username__icontains=user_search)
        return render(request,'admin/user_search.html',{'users':user})
    else:
        return redirect('admin_login')






#CATEGORIES
def category_list(request):
    brands = ProductBrands.objects.all()
    categories = ProductCategories.objects.all()
    context = {'brands':brands,'categories':categories}
    return render(request, 'admin/category_list.html', context)

def category_add(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        categories = ProductCategories(category_name=category_name)
        categories.save()
        return redirect('category_list')
    return render(request,'admin/category_list.html')

def category_edit(request):
    categories = ProductCategories.objects.all()
    context = {'categories':categories}
    return redirect('category_list',context)



def category_update(request,id):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        categories = ProductCategories(id=id, category_name=category_name)
        categories.save()           
        return redirect('category_list')          
    return render(request, 'admin/category_list.html')

def change_category_block_status(request, id):
    if request.method == 'POST':
        block_status = request.POST.get('block_status', False) == 'True'
        category = ProductCategories.objects.get(pk=id)
        category.is_blocked = block_status
        category.save()
        return redirect('category_list')


def category_delete(request,id):
    categories = ProductCategories.objects.filter(id=id)
    categories.delete()
    context = {'categories':categories}
    return redirect('category_list')


#BRANDS
def brand_list(request):
    brands = ProductBrands.objects.all()
    context = {'brands':brands}
    return render(request, 'admin/brand_list.html',context)

def brand_add(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brands = ProductBrands(brand_name=brand_name)
        brands.save()
        return redirect('brand_list')
    return render(request,'admin/brand_list.html')

def brand_edit(request):
    brands = ProductBrands.objects.all()
    context = {'brands':brands}
    return redirect('brand_list',context)

def brand_update(request,id):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brands = ProductBrands(id=id,brand_name=brand_name)
        brands.save()
        return redirect('brand_list')
    return render(request,'admin/brand_list.html')

def change_brand_block_status(request, id):
    if request.method == 'POST':
        block_status = request.POST.get('block_status', False) == 'True'
        brand = ProductBrands.objects.get(pk=id)
        brand.is_blocked = block_status
        brand.save()
        return redirect('brand_list')

def brand_delete(request,id):
    brands = ProductBrands.objects.filter(id=id)
    brands.delete()
    context = {'brands':brands}
    return redirect('brand_list')



#PRODUCTS
def product_list(request):
    products = Product.objects.all()
    brands=ProductBrands.objects.all()
    categories=ProductCategories.objects.all()
    genders=Gender.objects.all()
    context = {'products':products,'brands':brands,'categories':categories, 'genders':genders}
    return render(request, 'admin/product_list.html',context)    



def product_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('product_brand')
        category_id = request.POST.get('product_category')
        product_thumbnail = request.FILES.get('product_thumbnail')
        product_price = request.POST.get('product_price')
        gender_id = request.POST.get('product_gender')
        product_description = request.POST.get('product_description')
        product_brand=get_object_or_404(ProductBrands, id=brand_id)
        product_category=get_object_or_404(ProductCategories, id=category_id)
        product_gender = get_object_or_404(Gender, id=gender_id)
        products = Product(
            product_name = product_name,
            product_brand = product_brand,
            product_category = product_category,
            product_thumbnail = product_thumbnail,
            product_price = product_price,
            product_gender = product_gender,
            product_description = product_description
        )
        products.save()
        return redirect('product_list')
       

def product_delete(request,id):
    products = Product.objects.get(id=id)
    brands=ProductBrands.objects.all()
    categories=ProductCategories.objects.all()
    genders=Gender.objects.all()
    products.delete()
    genders=Gender.objects.all()
    context = {'products':products,'brands':brands,'categories':categories,'genders':genders}
    return redirect('product_list')

def product_edit(request):
    products = Product.objects.all()
    context = {'products':products}
    return redirect('product_list',context)



def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('product_brand')
        category_id = request.POST.get('product_category')
        product_price = request.POST.get('product_price')
        gender_id = request.POST.get('product_gender')
        product_description = request.POST.get('product_description')
        
        # Retrieve the updated 'product_thumbnail' field value
        product_thumbnail = request.FILES.get('product_thumbnail')
        
        # Update other product details
        product.product_name = product_name
        product.product_brand = get_object_or_404(ProductBrands, id=brand_id)
        product.product_category = get_object_or_404(ProductCategories, id=category_id)
        product.product_price = product_price
        product.product_gender = get_object_or_404(Gender, id=gender_id)
        product.product_description = product_description
        
        # Only update 'product_thumbnail' if a new file was provided
        if product_thumbnail:
            product.product_thumbnail = product_thumbnail
        
        # Save the updated product
        product.save()
        
        return redirect('product_list')
    
    return render(request, 'admin/product_list.html', {'product': product})




#COLORS

def color_list(request):
    colors = ProductColors.objects.all()
    context = {'colors':colors}
    return render(request, 'admin/color_list.html',context)


def color_add(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        colors = ProductColors(color_name=color_name)
        colors.save()
        return redirect('color_list')
    return render(request,'admin/color_list.html')


def color_edit(request):
    colors = ProductColors.objects.all()
    context = {'colors':colors}
    return redirect('color_edit',context)

def color_update(request,id):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        color_name = request.POST.get('color_name')
        colors = ProductColors(id=id,color_name=color_name)
        colors.save()
        return redirect('color_list')
    return render(request,'admin/color_list.html')


def color_delete(request,id):
    colors = ProductColors.objects.filter(id=id)
    colors.delete()
    context = {'colors':colors}
    return redirect('color_list')

#SIZE

def size_list(request):
    sizes = ProductSizes.objects.all()
    context = {'sizes':sizes}
    return render(request, 'admin/size_list.html',context)


def size_add(request):
    if request.method == 'POST':
        size_number = request.POST.get('size_number')
        sizes = ProductSizes(size_number=size_number)
        sizes.save()
        return redirect('size_list')
    return render(request,'admin/size_list.html')


def size_edit(request):
    sizes = ProductSizes.objects.all()
    context = {'sizes':sizes}
    return redirect('size_edit',context)

def size_update(request,id):
    if request.method == 'POST':
        size_number = request.POST.get('size_number')
        sizes = ProductSizes(id=id,size_number=size_number)
        sizes.save()
        return redirect('size_list')
    return render(request,'admin/size_list.html')


def size_delete(request,id):
    sizes = ProductSizes.objects.filter(id=id)
    sizes.delete()
    context = {'sizes':sizes}
    return redirect('size_list')


#PRODUCT IMAGES

def product_images_list(request):
    product_images = ProductImages.objects.all()
    products = Product.objects.all()
    colors = ProductColors.objects.all()
    context = {
        'products':products,
        'product_images':product_images,
        'colors':colors,
        }
    return render(request, 'admin/product_images.html',context) 


def product_images_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        color_id = request.POST.get('product_color')
        image_1 = request.FILES.get('product_image_1')
        image_2 = request.FILES.get('product_image_2')
        image_3 = request.FILES.get('product_image_3')

        product_name = get_object_or_404(Product, id=product_id)
        product_color=get_object_or_404(ProductColors, id=color_id)
        products = ProductImages(
            name = product_name,
            colors = product_color, 
            image_1 = image_1,
            image_2 = image_2,
            image_3 = image_3
        )
        products.save()
        return redirect('product_images_list')
    

    

def product_images_edit(request):
    product_images = ProductImages.objects.all()
    context = {'product_images':product_images}
    return redirect('product_images_list',context)


def product_images_update(request, id):
    product_images = get_object_or_404(ProductImages, id=id)    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        color_id = request.POST.get('product_color')      
        product_image_1 = request.FILES.get('product_image_1')
        product_image_2 = request.FILES.get('product_image_2')
        product_image_3 = request.FILES.get('product_image_3')       
        product_images.name = get_object_or_404(Product, product_name=product_name)
        product_images.colors = get_object_or_404(ProductColors, id=color_id)    
        if product_image_1:
            product_images.image_1 = product_image_1
        if product_image_2:
            product_images.image_2 = product_image_2
        if product_image_3:
            product_images.image_3 = product_image_3
        product_images.save()
        return redirect('product_images_list')
    return render(request, 'admin/product_images.html', {'product_images': product_images})

def product_images_delete(request,id):
    product_images = ProductImages.objects.get(id=id)
    product_images.delete()
    return redirect('product_images_list')


# PRODUCT VARIENTS


def product_varient_colors(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = Product.objects.get(id=product_id)
        product_image_objects = ProductImages.objects.filter(name=product)
        colors = list(map(lambda x: {'id': str(x.id), 'name': str(x.colors.color_name)}, list(product_image_objects)))
        print(product_image_objects[0].colors.color_name)
        return JsonResponse({'colors': colors})

def product_varients_list(request):
    product_varients = ProductVarient.objects.all()
    products = Product.objects.all()
    product_colors = ProductImages.objects.all()
    colors = ProductColors.objects.all()
    sizes = ProductSizes.objects.all()
    context = {
        'product_varients':product_varients,
        'products':products,
        'product_colors':product_colors,
        'sizes':sizes,
        'colors':colors,
        }
    print(product_colors[1].colors.color_name)
    print(product_colors[1].name.product_name)
    return render(request, 'admin/product_varients.html',context) 


def product_varients_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        size_id = request.POST.get('product_size')
        stock = request.POST.get('product_stock')
        color_id = request.POST.get('product_color')

        product_name = get_object_or_404(Product, id=product_id)
        product_size = get_object_or_404(ProductSizes, id=size_id)
        product_color = get_object_or_404(ProductImages, id=color_id)

        # Retrieve unique colors associated with the selected product
        product_images = ProductImages.objects.filter(name=product_name)
        unique_colors = product_images.values_list('colors__id', flat=True).distinct()
        colors = ProductColors.objects.filter(id__in=unique_colors)

        for color in colors:
            product_varient = ProductVarient(
                name=product_name,
                colors=product_color,
                size=product_size,
                stock=stock,
            )
            product_varient.save()

        return redirect('product_varients_list')
    

def product_varients_edit(request):
    product_varients = ProductVarient.objects.all()
    context = {'product_varients':product_varients}
    return redirect('product_varients_list',context)



def product_varients_update(request,id):
    product = get_object_or_404(ProductVarient, id=id)
    if request.method == 'POST':
        stock_number = request.POST.get('stock_number')
        product.stock = stock_number
        product.save()
        return redirect('product_varients_list')
    return render(request,'admin/product_varients.html')





def product_varients_delete(request,id):
    product_varients = ProductVarient.objects.get(id=id)
    product_varients.delete()
    return redirect('product_varients_list')


# ORDER

def order_list(request):
    orders = Orders.objects.all()
    order_items = OrderItem.objects.all()
    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()
    for i in order_items:
        print('order_no:',i.order_no)
    context = {'orders':orders,'order_items':order_items,'users':users, 'addresses':addresses, 'products':products, 'singleproducts':singleproducts}
    return render(request, 'admin/order_list.html',context)  

def order_edit(request):
    orders = Orders.objects.all()
    context = {'orders':orders}
    return redirect('order_list', context)

def order_update(request,id):
    order_status = get_object_or_404(Orders, id=id)
    if request.method == 'POST':
        status = request.POST.get('order_status')
        order_status.order_status = status
        order_status.save()
        return redirect('order_list')
    return render(request, 'admin/order_list.html')


#COUPON

def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {'coupons':coupons}
    return render(request, 'admin/coupon_list.html',context)


def coupon_add(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        active = request.POST.get('active')   
        discount=Decimal(discount)     
        coupons = Coupon(
            code=code,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            active=active
            )
        coupons.save()
        return redirect('coupon_list')
    return render(request,'admin/coupon_list.html')


def coupon_edit(request):
    coupons = Coupon.objects.all()
    context = {'coupons':coupons}
    return redirect('color_edit',context)

def coupon_update(request,id):
    coupons = get_object_or_404(Coupon, id=id)
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        status = request.POST.get('status')
        
        coupons.code = code
        coupons.discount = discount
        coupons.valid_from = valid_from
        coupons.valid_to = valid_to
        coupons.active = status
        coupons.save()
        return redirect('coupon_list')
    return render(request,'admin/coupon_list.html')


def coupon_delete(request,id):
    coupons = Coupon.objects.filter(id=id)
    coupons.delete()
    context = {'coupons':coupons}
    return redirect('coupon_list')





def order_list_today(request):
    today = date.today()
    orders = Orders.objects.filter(order_date__date=today)
    order_items = OrderItem.objects.filter(order_no__order_date__date=today)
    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()
    context = {'orders': orders, 'order_items': order_items, 'users': users, 'addresses': addresses, 'products': products, 'singleproducts': singleproducts}
    return render(request, 'admin/order_list.html', context)



def order_list_monthly(request):
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    orders = Orders.objects.filter(
        order_date__range=[start_of_month, end_of_month]
    )
    order_items = OrderItem.objects.filter(
        order_no__order_date__range=[start_of_month, end_of_month]
    )
    
    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'addresses': addresses,
        'products': products,
        'singleproducts': singleproducts
    }
    
    return render(request, 'admin/order_list.html', context)




def order_list_yearly(request):
    today = date.today()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    
    orders = Orders.objects.filter(
        order_date__year=today.year
    )
    order_items = OrderItem.objects.filter(
        order_no__order_date__year=today.year
    )
    
    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'addresses': addresses,
        'products': products,
        'singleproducts': singleproducts
    }
    
    return render(request, 'admin/order_list.html', context)



def order_list_weekly(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    orders = Orders.objects.filter(
        order_date__range=[start_of_week, end_of_week]
    )
    order_items = OrderItem.objects.filter(
        order_no__order_date__range=[start_of_week, end_of_week]
    )
    
    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()
    
    context = {
        'orders': orders,
        'order_items': order_items,
        'users': users,
        'addresses': addresses,
        'products': products,
        'singleproducts': singleproducts
    }
    
    return render(request, 'admin/order_list.html', context)


from datetime import datetime

def order_list_within_duration(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    users = Account.objects.all()
    addresses = MultipleAddresses.objects.all()
    products = ProductVarient.objects.all()
    singleproducts = Product.objects.all()

    print("Start Date:", start_date)
    print("End Date:", end_date)

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        print("Formatted Start Date:", start_date)
        print("Formatted End Date:", end_date)

        orders = Orders.objects.filter(order_date__range=[start_date, end_date])
        order_items = OrderItem.objects.filter(order_no__order_date__range=[start_date, end_date])

        print("Filtered Orders:", orders)
        print("Filtered Order Items:", order_items)

        context = {
            'orders': orders,
            'order_items': order_items,
            'users': users,
            'addresses': addresses,
            'products': products,
            'singleproducts': singleproducts
        }

        return render(request, 'admin/order_list.html', context)

    return render(request, 'admin/order_list.html', {'users': users, 'addresses': addresses, 'products': products, 'singleproducts': singleproducts})





# def fromtosales(request):
#     if request.method == 'POST':
#         from_date = request.POST.get('fromDate')
#         to_date = request.POST.get('toDate')
#     orders = Order.objects.filter(order_date__range=[from_date, to_date])
#     total_amount = sum(order.payment_amount for order in orders)
#     context= {
#         'total_payment_amount': total_amount,
#         'orders': orders
#     }
#     return render(request,'admin/sales_report.html',context)



