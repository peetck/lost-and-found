from rest_framework import serializers

from .models import Post, PostPicture, AssetType, Comment

class PostPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPicture
        fields = ['picture']

class PostSerializer(serializers.ModelSerializer):
    assetType = serializers.ReadOnlyField(source='assetType.name')
    user = serializers.ReadOnlyField(source='user.username')
    pictures = PostPictureSerializer(source='postpicture_set', many=True)
    class Meta:
        model = Post
        fields = '__all__'

class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ReadOnlyField(source='user.userprofile.avatar.url')
    class Meta:
        model = Comment
        fields = '__all__'

