from django import forms
from .models import Account
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class'       : 'form-control',
        

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter First Name',
        'class'       : 'form-control',
        
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Last Name',
        'class'       : 'form-control',
        
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Enter Email Address',
        'class'       : 'form-control',
    
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Phone Number ',
        'class'       : 'form-control',
    
    }))
    class Meta:
        model   = Account
        fields  = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):   
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class'       : 'form-control',
        

    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Enter Email Address',
        'class'       : 'form-control',
    
    }))
    class Meta:
        model   = Account
        fields  = ['email', 'password']


# def __init__(self, *args, **kwargs):
#     super(RegistrationForm, self).__init__(*args, **kwargs)
#     self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
#     self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
#     self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
#     self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
#     for field in self.fields:
#         self.fields[field].widget.attrs['class'] = 'form-control'


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')