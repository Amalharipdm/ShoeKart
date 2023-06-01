from django.urls import path
from . import views

urlpatterns = [
    path('user_login', views.user_login, name='user_login'),
    path('user_register', views.user_register, name='user_register'),
    path('otp_verification', views.otp_verification, name='otp_verification'),
    path('user_logout', views.user_logout, name='user_logout'),

    path('profile_view', views.profile_view, name='profile_view'),
    path('change_password', views.change_password, name='change_password'),

]