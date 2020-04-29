from django.contrib import admin
from .models import UserProfile, Faculty
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'faculty',
        'avatar'
    ]

class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'faculty_name'
    ]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Faculty, FacultyAdmin)