from django.urls import path
from . import views

urlpatterns = [
    path('cart_home', views.cart_home, name='cart_home'),
    # path('add_cart/<int:product_id>/', views.add_cart, name='add_cart')

]