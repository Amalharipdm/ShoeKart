import random
import smtplib
import ssl
from django.shortcuts import render,redirect
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

# Create your views here.

# 




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


# def user_login(request):
#     return render(request, 'accounts/user.html')



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

# def user_logout(request):
#     if 'email' in request.session:
#          del request.session['email']
#     return redirect('user_login')

def user_logout(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = Account.objects.get(email=email)
            if user.is_blocked:
                # User is blocked, display a message
                messages.error(request, 'Your account has been blocked by the admin.')
                return redirect('user_login')  # Replace 'user_login' with your login URL
        except Account.DoesNotExist:
            pass
        
        del request.session['email']
    return redirect('user_login') 


# def user_register(request):
#     global fname
#     global lname
#     global e_mail
#     global uname
#     global pwd1
#     if 'username' in request.session:
#         return redirect('index')
    
#     if request.method == 'POST':
#         fname = request.POST.get('first_name')
#         lname = request.POST.get('last_name')
#         e_mail = request.POST.get('email')
#         uname = request.POST.get('username')
#         pwd1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
        
#         if not uname or not pwd1 or not password2:
#             messages.warning(request, "Please fill all the required fields.")
#         elif pwd1 != password2:
#             messages.warning(request, 'Passwords do not match.')       
#         elif User.objects.filter(username=uname).exists():
#             messages.warning(request,'Username already taken')
#         elif User.objects.filter(email=e_mail).exists():
#             messages.warning(request, 'Email already taken')  
#         else:      
#             otp = random.randint(100000, 999999)
#             request.session['otp'] = str(otp)
#             send_mail(
#                 'OTP Verification',
#                 'Your OTP is ' + str(otp),
#                 'amalharissc@gmail.com',
#                 [e_mail],
#                 fail_silently=False,
#             )
#             return redirect('otp_verification')
#     return render(request, 'accounts/user_register.html')
 

# def user_login(request):
#     if 'username' in request.session:
#         return redirect('index')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             request.session['username']=username
#             return redirect('index')
#         else:
#             return render(request, 'accounts/user_login.html', {'error': 'Invalid username or password'})
#     else:
#         return render(request, 'accounts/user_login.html')
    

# def user_logout(request):
#     if 'username' in request.session:
#         del request.session['username']
#     return redirect('user_login')


# def otp_verification(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if otp == request.session.get('otp'):
#             user = User.objects.create_user(username=uname, email=e_mail, password=pwd1, first_name=fname, last_name=lname)
#             user.save()
#             return redirect('user_login')
#         else:
#             context = {'error': 'Invalid OTP. Please try again.'}
#             return render(request, 'accounts/otp_verification.html', context)
#     return render(request, 'accounts/otp_verification.html') 


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
