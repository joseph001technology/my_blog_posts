from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Post
from accounts.models import Profile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff',]

 


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content','image', 'published_at', 'author', 'status', 'slug','created_at', 'updated_at', 'excerpt',)
        
        
        # accounts/serializers.py
 

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    # or serializers.PrimaryKeyRelatedField if you prefer IDs

    class Meta:
        model = Profile
        fields = ["id", "user", "avatar", "bio"]
