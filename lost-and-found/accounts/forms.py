from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    username = forms.CharField(
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'ชื่อผู้ใช้งาน'}),
        label = 'ชื่อผู้ใช้งาน'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อจริง'}),
        max_length=32,
        label = 'ชื่อจริง'

    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'นามสกุล'}),
        max_length=32,
        label='นามสกุล'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='อีเมล์'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'รหัสผ่าน'}),
        label='รหัสผ่าน'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'ยืนยันรหัสผ่าน'}),
        label='ยืนยันรหัสผ่าน'
    )
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'รหัสผ่านเก่า'}),
        label='รหัสผ่านเก่า'
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'รหัสผ่านใหม่'}),
        label='รหัสผ่านใหม่'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'ยืนยันรหัสผ่าน'}),
        label='ยืนยันรหัสผ่าน'
    )

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อจริง'}),
        max_length=32,
        label = 'ชื่อจริง'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'นามสกุล'}),
        max_length=32,
        label='นามสกุล'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='อีเมล์'
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")