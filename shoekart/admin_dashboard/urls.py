from django.urls import path
from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_edit/<int:id>', views.user_edit, name='user_edit'),
    path('user_search', views.user_search, name='user_search'),
    path('block_user/<int:id>', views.block_user, name='block_user'),
    path('unblock_user/<int:id>', views.unblock_user, name='unblock_user'),
    path('category_list', views.category_list,name='category_list'),
    path('category_add', views.category_add,name='category_add'),
    path('category_edit', views.category_edit,name='category_edit'),
    path('category_update/<str:id>',views.category_update,name='category_update'),
    path('category_delete/<str:id>', views.category_delete,name='category_delete'),
    path('change_category_block_status/<str:id>', views.change_category_block_status,name='change_category_block_status'),
    path('brand_list', views.brand_list,name='brand_list'),
    path('brand_add', views.brand_add,name='brand_add'),
    path('brand_edit', views.brand_edit,name='brand_edit'),
    path('brand_update/<str:id>',views.brand_update,name='brand_update'),
    path('brand_delete/<str:id>', views.brand_delete,name='brand_delete'),
    path('change_brand_block_status/<str:id>', views.change_brand_block_status,name='change_brand_block_status'),
    path('product_list', views.product_list,name='product_list'),
    path('product_add', views.product_add,name='product_add'),
    path('product_delete/<str:id>', views.product_delete,name='product_delete'),
    path('product_edit', views.product_edit,name='product_edit'),
    path('product_update/<str:id>',views.product_update,name='product_update'),
    path('color_list', views.color_list,name='color_list'),
    path('color_add', views.color_add,name='color_add'),
    path('color_edit', views.color_edit,name='color_edit'),
    path('color_update/<str:id>',views.color_update,name='color_update'),
    path('color_delete/<str:id>', views.color_delete,name='color_delete'),
    path('size_list', views.size_list,name='size_list'),
    path('size_add', views.size_add,name='size_add'),
    path('size_edit', views.size_edit,name='size_edit'),
    path('size_update/<str:id>',views.size_update,name='size_update'),
    path('size_delete/<str:id>', views.size_delete,name='size_delete'),
    path('product_images_list', views.product_images_list,name='product_images_list'),
    path('product_images_add', views.product_images_add,name='product_images_add'),
    path('product_images_delete/<str:id>', views.product_images_delete,name='product_images_delete'),
    path('product_images_edit', views.product_images_edit,name='product_images_edit'),
    path('product_images_update/<str:id>',views.product_images_update,name='product_images_update'),
    path('product_varients_list', views.product_varients_list,name='product_varients_list'),
    path('product_varients_add', views.product_varients_add,name='product_varients_add'),
    path('product_varient_colors', views.product_varient_colors ,name='product_varient_colors'),
    path('product_varients_delete/<str:id>', views.product_varients_delete,name='product_varients_delete'),
    path('product_varients_edit', views.product_varients_edit,name='product_varients_edit'),
    path('product_varients_update/<str:id>',views.product_varients_update,name='product_varients_update'),
    path('order_list', views.order_list,name='order_list'),
    path('order_edit', views.order_edit,name='order_edit'),
    path('order_update/<str:id>', views.order_update,name='order_update'),

    path('coupon_list', views.coupon_list,name='coupon_list'),
    path('coupon_add', views.coupon_add,name='coupon_add'),
    path('coupon_edit', views.coupon_edit,name='coupon_edit'),
    path('coupon_update/<str:id>',views.coupon_update,name='coupon_update'),
    path('coupon_delete/<str:id>', views.coupon_delete,name='coupon_delete'),


    path('order_list_today', views.order_list_today, name='order_list_today'),
    path('order_list_monthly', views.order_list_monthly, name='order_list_monthly'),
    path('order_list_yearly', views.order_list_yearly, name='order_list_yearly'),
    path('order_list_weekly', views.order_list_weekly, name='order_list_weekly'),
    path('order_list_within_duration', views.order_list_within_duration, name='order_list_within_duration'),



]