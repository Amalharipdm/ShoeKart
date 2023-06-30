import random
import smtplib
import ssl
from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from .forms import PasswordResetForm
import json
from .models import Account
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from cart_detail.models import *    

# Create your views here.


def user_register(request):
    if 'email' in request.session:
        return redirect('index')    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            check_user = Account.objects.filter(email=email).first()
            if check_user:
                messages.warning(request, "Email already exists")
                return redirect('user_register')
            
            request.session['registration_form_data'] = form.cleaned_data
            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)
            send_mail(
                'OTP Verification',
                'Your OTP is ' + str(otp),
                'amalharissc@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp_verification')
    
    form = RegistrationForm()
    return render(request, 'accounts/user_register.html', {'form': form})



def otp_verification(request):
    if 'otp' in request.session: 
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if otp == request.session.get('otp'):
                form_data = request.session.get('registration_form_data')
                form = RegistrationForm(form_data)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = user.email.split("@")[0]
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Registration Successful')
                    request.session.flush()
                    return redirect('user_login')
                else:
                    messages.error(request, 'Invalid form data')
                    return redirect('user_register')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('otp_verification')
        return render(request, 'accounts/otp_verification.html')
    else:
        return redirect('user_register')






def user_login(request):
    if 'email' in request.session:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session['email']=email

            return redirect('index')           
        else:
            messages.error(request,'invalid login credentials')
            return redirect('user_login')
    else:
        return render(request, 'accounts/user_login.html')



def user_logout(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = Account.objects.get(email=email)
            if user.is_blocked:
                messages.error(request, 'Your account has been blocked by the admin.')
                return redirect('user_login')  
        except Account.DoesNotExist:
            pass
        
        del request.session['email']
    return redirect('user_login') 




def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.postcode = request.POST.get('postcode')
        user.address_line_1 = request.POST.get('address_line_1')
        user.address_line_2 = request.POST.get('address_line_2')
        user.area = request.POST.get('area')
        user.state = request.POST.get('state')
        user.save()

        messages.success(request, 'Your profile has been updated.')
        return redirect('profile_view')
    return render(request, 'accounts/profile_view.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your Password has been changed successfully.')
            return redirect('profile_view')
        
    else:
        form = PasswordChangeForm(request.user)
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f'{field}: {error}')
    context = {
        'form': form
    }
    return render(request, 'accounts/profile_view.html', context)
    


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                user = None

            if user is not None:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                current_site = get_current_site(request)
                mail_subject = 'Password Reset Request'
                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                send_mail(mail_subject, message, 'amalharissc@gmail.com', [email])

                messages.success(request, 'Password reset email has been sent. Please check your email.')
                return redirect('password_reset_confirmation')+ f'?email={email}'
            else:
                messages.error(request, 'No user found with the provided email address.')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset_form.html', {'form': form})



def password_reset_confirmation(request):
    email = request.GET.get('email')  
    return render(request, 'password_reset_confirmation.html', {'email': email})




def profile(request):
    return render(request, 'accounts/profile.html')


def display_addresses_profile(request):
    addresses = MultipleAddresses.objects.filter(user=request.user)
    
    context = {
        'addresses': addresses,
    }
    return render(request, 'accounts/show_addresses.html', context)

def profile_view_demo(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.postcode = request.POST.get('postcode')
        user.address_line_1 = request.POST.get('address_line_1')
        user.address_line_2 = request.POST.get('address_line_2')
        user.area = request.POST.get('area')
        user.state = request.POST.get('state')
        user.save()

        messages.success(request, 'Your profile has been updated.')
        return redirect('profile')
    return render(request, 'accounts/profile.html')



def profile_order_detail(request):
    user = request.user
    orders = Orders.objects.filter(user=user)

    context = {
        'orders': orders
    }

    return render(request, 'accounts/show_order.html', context)


def cancel_order_item(request,id):
    order_item = OrderItem.objects.get(id=id)
    order_item.status = 'Cancelled'
    order_item.delete()

    order = order_item.order_no
    remaining_order_items = order.orderitem_set.exists()
    if not remaining_order_items:
        order.delete()
        return redirect('profile_order_detail')
    return redirect('profile_order_detail')

