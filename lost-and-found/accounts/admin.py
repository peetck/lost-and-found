from django.contrib import admin
from .models import UserProfile, Faculty
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Faculty)