from django.shortcuts import render
from django.http import HttpResponse
from products.models import *
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

def shop_home(request):
    products = Product.objects.all()
    categories = ProductCategories.objects.all()
    genders = Gender.objects.all()
    brands = ProductBrands.objects.all()

    paginator = Paginator(products, per_page=3)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'products':page_products,
        'categories':categories,
        'genders':genders,
        'brands':brands
        }
    return render(request,'products/shop.html', context)

def products_by_brand(request,id):
    products = Product.objects.filter(product_brand=id)
    categories = ProductCategories.objects.all()
    genders = Gender.objects.all()
    brands = ProductBrands.objects.all()
    context = {
        'products':products,
        'categories':categories,
        'genders':genders,
        'brands':brands
        }
    return render(request,'products/products_by_brand.html', context)

def products_by_category(request,id):
    products = Product.objects.filter(product_category=id)
    categories = ProductCategories.objects.all()
    genders = Gender.objects.all()
    brands = ProductBrands.objects.all()
    context = {
        'products':products,
        'categories':categories,
        'genders':genders,
        'brands':brands
        }
    return render(request,'products/products_by_category.html', context)


def products_by_gender(request,id):
    products = Product.objects.filter(product_gender=id)
    categories = ProductCategories.objects.all()
    genders = Gender.objects.all()
    brands = ProductBrands.objects.all()
    context = {
        'products':products,
        'categories':categories,
        'genders':genders,
        'brands':brands
        }
    return render(request,'products/products_by_gender.html', context)

def product_detail(request,id):
    products = Product.objects.get(id=id)
    product_images = ProductImages.objects.filter(name=products)
    colors = ProductImages.objects.filter(name=products).values_list('colors__color_name', flat=True).distinct()
    selected_color = request.GET.get('color')
    selected_varient = request.GET.get('size')
    product_varients = ProductVarient.objects.filter(name=products)
    for i in range(0,len(product_images)):
        product_images[i].str_colors = str(product_images[i].colors)
    if not selected_color:
        selected_color = product_images[0].str_colors
    varients = ProductVarient.objects.filter(name = products)
    str_varients = []
    for i in range(0, len(varients)):
        if (str(varients[i].colors) == selected_color):
            str_varients.append(str(varients[i].size)) 

    if not selected_varient:
        selected_varient = str_varients[0]
    the_color = selected_color
    the_size = int(selected_varient)
    my_varient = None
    for i in range(0, len(product_varients)):
        if product_varients[i].colors.colors.color_name == the_color and product_varients[i].size.size_number == the_size:
            my_varient = product_varients[i]
            break    
    context = {
        'products':products, 
        'product_images':product_images,
        'varients':varients,
        'str_varients':str_varients,
        'colors' : colors,
        'selected_color': selected_color,
        'selected_varient': selected_varient,
        'my_varient_id': str(my_varient.id),
        }
    return render(request,'products/product_detail.html', context)








def filtered_products(request):
    selected_genders = request.GET.getlist('gender')
    selected_category = request.GET.get('category')
    selected_brand = request.GET.get('brand')   
    products = Product.objects.all()   
    if selected_genders:
        products = products.filter(product_gender__in=selected_genders)
    if selected_category:
        products = products.filter(product_category__in =selected_category)
    if selected_brand:
        products = products.filter(product_brand__in=selected_brand)   
    categories = ProductCategories.objects.all()
    genders = Gender.objects.all()
    brands = ProductBrands.objects.all()    
    context = {
        'products': products,
        'categories': categories,
        'genders': genders,
        'brands': brands
    }    
    return render(request, 'products/shop.html', context)






# def product_search(request):
#     if request.method == 'GET':
#         product_search = request.GET.get('product_search')
#         user = Product.objects.filter(username__icontains=user_search)
#         return render(request,'admin/user_search.html',{'users':user})
#     else:
#         return redirect('admin_login')


# def add_cart(request,product_id):
#     color = request.GET['color']
#     size = request.GET['size']
#     return HttpResponse(color + ' ' + size)
#     exit()
