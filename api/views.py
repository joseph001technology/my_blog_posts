from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from accounts.models import Profile
from blog.models import Post

from .serializers import PostsSerializer, ProfileSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer