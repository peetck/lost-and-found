from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    date_time = forms.DateField(input_formats=['%d/%m/%Y'])
    class Meta:
        model = Post
        exclude = ['user', 'is_active']

