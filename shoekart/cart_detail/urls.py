from django.urls import path
from . import views

urlpatterns = [
    
    
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
   
    
    path('cart_view', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    # path('update_cart_item', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    
    path('display_addresses', views.display_addresses, name='display_addresses'),
    path('add_address', views.add_address, name='add_address'),
    path('user-address', views.use_address, name='use_address'),
    path('use_address/<int:address_id>/', views.use_address, name='use_address'),
    path('address_edit', views.address_edit,name='address_edit'),
    path('address_update/<str:id>',views.address_update,name='address_update'),
    path('address_delete/<str:id>', views.address_delete,name='address_delete'),

    path('address_home', views.address_home, name='address_home'),


    path('place_order', views.place_order, name='place_order'),
    path('order_detail/<uuid:order_id>/', views.order_detail, name='order_detail'),

    path('razorpay_payment', views.razorpay_payment, name='razorpay_payment'),

    path('order_detail', views.order_detail, name='order_detail'),
    path('apply_coupon/<int:coupon_id>', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon_view', views.remove_coupon_view, name='remove_coupon_view')



    ]