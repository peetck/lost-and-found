from django.contrib import admin

from .models import Post, AssetType, PostPicture, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(AssetType)
admin.site.register(PostPicture)
admin.site.register(Comment)