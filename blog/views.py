from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    all_posts = Post.newmanager.all()
    return render(request, 'index.html', {'posts': all_posts})

def post_single(request, slug):  # <== This must be 'slug'
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'single.html', {'post': post})

def logout_success(request):
    return render(request, 'logout_success.html')
def personal_home(request):
    return render(request, 'home.html')