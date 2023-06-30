from django.urls import path
from . import views

urlpatterns = [
    path('shop_home', views.shop_home, name='shop_home'),
    path('products_by_brand/<int:id>', views.products_by_brand, name='products_by_brand'),
    path('products_by_category/<int:id>', views.products_by_category, name='products_by_category'),
    path('products_by_gender/<int:id>', views.products_by_gender, name='products_by_gender'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('filtered_products', views.filtered_products, name='filtered_products'),
    path('search_products', views.search_products, name='search_products'),



]