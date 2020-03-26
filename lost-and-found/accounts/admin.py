from django.contrib import admin
from .models import UserProfilePicture, Faculty, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

admin.site.register(UserProfilePicture)
admin.site.register(Faculty)
admin.site.register(CustomUser)