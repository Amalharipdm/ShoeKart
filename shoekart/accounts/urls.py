from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user_login', views.user_login, name='user_login'),
    path('user_register', views.user_register, name='user_register'),
    path('otp_verification', views.otp_verification, name='otp_verification'),
    path('user_logout', views.user_logout, name='user_logout'),

    path('profile_view', views.profile_view, name='profile_view'),
    path('change_password', views.change_password, name='change_password'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/<str:uid64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done.', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




]