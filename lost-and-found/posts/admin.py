from django.contrib import admin

from .models import Post, AssetType, PostPicture, Comment

# Register your models here.

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'desc',
        'date_time',
        'location',
        'key',
        'create_at'
    ]

class PostPictureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'post',
        'picture'
    ]

class CommendAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'post',
        'msg',
        'user',
        'create_at'
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(PostPicture, PostPictureAdmin)
admin.site.register(Comment, CommendAdmin)