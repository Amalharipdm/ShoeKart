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

]