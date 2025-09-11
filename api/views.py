from django.shortcuts import render
from blog.models import Post
from accounts.models import Profile
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, PostsSerializer, ProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer