from django.db import models
from django.contrib.auth.models import User
# accounts app

# Create your models here.

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)# reference to User Table

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

class UserProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # reference to User Table
    avatar = models.ImageField(default='')