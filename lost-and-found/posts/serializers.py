from rest_framework import serializers

from .models import Post, PostPicture, AssetType

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
