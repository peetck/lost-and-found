from django.db import models
from django.contrib.auth.models import User
# posts app

# Create your models here.


class AssetType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    is_active = models.BooleanField(default=True)
    TYPE = (
        ('found', 'เจอของหาย'),
        ('lost', 'ตามหาของ'),
    )
    type = models.CharField(choices=TYPE, max_length=255, default='found')
    date_time = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    desc = models.TextField()
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact1 = models.CharField(max_length=255)
    contact2 = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    assetType = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class PostPicture(models.Model):
    picture = models.ImageField(default='posts/post_default.png', upload_to='posts/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

