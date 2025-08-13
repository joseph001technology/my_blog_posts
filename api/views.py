from django.shortcuts import render
from blog.models import Post
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, PostsSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer