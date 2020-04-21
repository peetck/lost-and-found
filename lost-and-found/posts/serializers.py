from rest_framework import serializers

from .models import Post, PostPicture

class PostSerializer(serializers.ModelSerializer):

    assetType = serializers.ReadOnlyField(source='assetType.name')
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Post
        fields = "__all__"

class PostPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPicture
        fields = ['post', 'picture']