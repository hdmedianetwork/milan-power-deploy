from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

ROLE_CHOICE = (
    ('salesman', 'Salesman'),
    ('receiver', 'Receiver'),
    ('checker', 'Checker'),
    ('accountant', 'Accountant')
) 

class UserRegisterForm(UserCreationForm):
    usable_password = None # To hide the unecessary field
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(choices=ROLE_CHOICE, widget=forms.Select(attrs={'class': 'form-select mb-3'}))

    class Meta:
        model = User
        fields = ['email', 'username']
        # fields = '__all__'
    