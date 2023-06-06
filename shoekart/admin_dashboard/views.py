from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate, logout
from products.models import *
from accounts.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user.is_admin:
           login(request,user)
           return redirect('admin_home')
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')

    return render(request,"admin/admin_login.html")

def admin_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_login')

@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
    return render(request,"admin/admin_home.html")

   





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
    # products = Product.objects.all()
    # context = {
    #     'products':products,
    # }
    # return render(request, 'admin/product_list.html', context)    

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

# def product_update(request,id):
#     if request.method == 'POST':
#         product_name = request.POST.get('product_name')
#         brand_id = request.POST.get('product_brand')
#         category_id = request.POST.get('product_category')
#         product_thumbnail = request.FILES.get('product_thumbnail')
#         product_price = request.POST.get('product_price')
#         gender_id = request.POST.get('product_gender')
#         product_description = request.POST.get('product_description')
#         product_brand=get_object_or_404(ProductBrands, id=brand_id)
#         product_category=get_object_or_404(ProductCategories, id=category_id)
#         product_gender = get_object_or_404(Gender, id=gender_id)
#         products = Product(id=id,
#             product_name = product_name,
#             product_brand = product_brand,
#             product_category = product_category,
#             product_thumbnail = product_thumbnail,
#             product_price = product_price,
#             product_gender = product_gender,
#             product_description = product_description
#         )
#         products.save()
#         return redirect('product_list')
#     return render(request,'admin/product_list.html')

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

def product_varient_colors(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = Product.objects.get(id=product_id)
        product_image_objects = ProductImages.objects.filter(name=product)
        colors = list(map(lambda x: str(x), list(product_image_objects)))
        print(list)
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


from django.shortcuts import get_object_or_404

def product_varients_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        size_id = request.POST.get('product_size')
        stock = request.POST.get('product_stock')

        product_name = get_object_or_404(Product, id=product_id)
        product_size = get_object_or_404(ProductSizes, id=size_id)

        # Retrieve unique colors associated with the selected product
        product_images = ProductImages.objects.filter(name=product_name)
        unique_colors = product_images.values_list('colors__id', flat=True).distinct()
        colors = ProductColors.objects.filter(id__in=unique_colors)

        for color in colors:
            product_varient = ProductVarient(
                name=product_name,
                colors=color,
                size=product_size,
                stock=stock,
            )
            product_varient.save()

        return redirect('product_varients_list')
