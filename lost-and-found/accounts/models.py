from django.db import models
from django.contrib.auth.models import User
# accounts app

# Create your models here.

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)

    def __str__(self):
        return self.faculty_name

class UserProfile(models.Model):
    avatar = models.ImageField(default='accounts/default.png') # Picture of user
    user = models.OneToOneField(User, on_delete=models.CASCADE) # reference to User Table
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE) # reference to Faculty Table