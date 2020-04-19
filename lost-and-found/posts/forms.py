from django import forms
from .models import Post, PostPicture
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    date_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label='วันและเวลา')
    date_time.widget.attrs = {'class' : 'form-control datetimepicker-input', 'data-target' : '#datetimepicker'}
    class Meta:
        model = Post
        fields = ['is_active','title','desc', 'type', 'assetType', 'date_time','location', 'contact1', 'contact2']

        widgets = {
            'desc' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'รายละเอียดต่างๆ เช่น คุณลักษณะเป็นยังไง เป็นต้น'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'ชื่อโพสต์'}),
            'is_active': forms.CheckboxInput(attrs={'class' : ''}),
            'location' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'สถานที่ เช่น ห้องนํ้า เป็นต้น'}),
            'contact1' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'xxx-xxx-xxxx'}),
            'contact2' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'example@example.com'}),
            'type' : forms.Select(attrs={'class' : 'form-control'}),
            'assetType' : forms.Select(attrs={'class' : 'form-control'}),
        }

        labels = {
            'desc' : 'รายละเอียด',
            'title' : 'ชื่อโพสต์',
            'is_active' : 'สภานะโพสต์ เปิด/ปิด',
            'location' : 'สถานที่',
            'contact1' : 'เบอร์ติดต่อ',
            'contact2' : 'อีเมล์',
            'type' : 'ประเภทของโพสต์',
            'assetType' : 'ประเภทของสิ่งของ',
        }

class PostPictureForm(forms.ModelForm):
    class Meta:
        model = PostPicture
        fields = ['picture']

        widgets = {
            'picture' : forms.FileInput(attrs={'class' : 'custom-file-input'})
        }


