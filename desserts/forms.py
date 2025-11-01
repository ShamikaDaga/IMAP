from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=20, required=True)
    card_number = forms.CharField(max_length=16, required=True)
    card_expiry = forms.CharField(max_length=5, required=True, help_text='MM/YY')
    card_cvv = forms.CharField(max_length=4, required=True)
