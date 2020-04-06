from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    date_time = forms.DateField(input_formats=['%d/%m/%Y'])
    date_time.widget.attrs = {'class' : 'form-control'}
    class Meta:
        model = Post
        exclude = ['user', 'is_active', 'key']

        widgets = {
            'desc' : forms.Textarea(attrs={'class' : 'form-control'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'location' : forms.TextInput(attrs={'class' : 'form-control'}),
            'contact1' : forms.TextInput(attrs={'class' : 'form-control'}),
            'contact2' : forms.TextInput(attrs={'class' : 'form-control'}),
            'type' : forms.Select(attrs={'class' : 'form-control'}),
            'assetType' : forms.Select(attrs={'class' : 'form-control'})
        }


