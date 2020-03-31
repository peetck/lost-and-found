from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Username'}),
        label = 'ชื่อผู้ใช้งาน'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=32,
        help_text='First name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=32,
        help_text='Last name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        max_length=64,
        help_text='Enter a valid email address'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'})
    )
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")