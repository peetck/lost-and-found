from django.db import models
from django.contrib.auth.models import User
# posts app

# Create your models here.


class AssetType(models.Model):
    name = models.CharField(max_length=255)

class Post(models.Model):
    is_active = models.BooleanField()
    TYPE = (
        ('lost', 'Lost'),
        ('found', 'Found')
    )
    type = models.CharField(choices=TYPE, max_length=255)
    date_time = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    desc = models.TextField()
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact1 = models.CharField(max_length=255)
    contact2 = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostPicture(models.Model):
    class Meta:
        unique_together = ('id', 'picture')
    id = models.IntegerField(primary_key=True)
    picture = models.ImageField(default='')

