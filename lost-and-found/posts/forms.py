from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    date_time = forms.DateField(input_formats=['%d/%m/%Y'], label='วันที่')
    date_time.widget.attrs = {'class' : 'form-control', 'placeholder' : 'dd/mm/yy'}
    class Meta:
        model = Post
        fields = ['title', 'type', 'desc', 'assetType', 'location', 'date_time', 'contact1', 'contact2']

        widgets = {
            'desc' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'รายละเอียดต่างๆ เช่น คุณลักษณะเป็นยังไง เป็นต้น'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'ชื่อโพสต์'}),
            'location' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'สถานที่ เช่น ห้องนํ้า เป็นต้น'}),
            'contact1' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'xxx-xxx-xxxx'}),
            'contact2' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'example@example.com'}),
            'type' : forms.Select(attrs={'class' : 'form-control'}),
            'assetType' : forms.Select(attrs={'class' : 'form-control'}),
        }

        labels = {
            'desc' : 'รายละเอียด',
            'title' : 'ชื่อโพสต์',
            'location' : 'สถานที่',
            'contact1' : 'เบอร์ติดต่อ',
            'contact2' : 'อีเมล์',
            'type' : 'ประเภทของโพสต์',
            'assetType' : 'ประเภทของสิ่งของ',
        }


