from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    # Add other required fields
