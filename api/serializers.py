from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Post
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

 


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content','image', 'published_at', 'author', 'status', 'slug','created_at', 'updated_at', 'excerpt')