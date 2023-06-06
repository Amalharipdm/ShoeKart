from django.urls import path
from . import views

urlpatterns = [
    path('cart_view', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('address_details', views.address_details, name='address_details')
    
    ]