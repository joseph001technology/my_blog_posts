from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from allauth.socialaccount.providers.google.views import oauth2_login
from .models import Post
from django.contrib.auth.decorators import login_required

def test_func(self):
    user = self.request.user
    return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)


def home(request):
    all_posts = Post.newmanager.all()
    return render(request, 'blogtemplates/index.html', {'posts': all_posts})
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)


def post_single(request, slug):  # <== This must be 'slug'
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blogtemplates/single.html', {'post': post})

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)

    
    

def logout_success(request):
    return render(request, 'blogtemplates/logout_success.html')

@login_required
def personal_home(request):
    return render(request, 'blogtemplates/home.html')

class AddView(CreateView):
    model = Post
    template_name = 'blogtemplates/add.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:homepage')
    
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)


class EditView(UpdateView):
    model = Post
    template_name = 'blogtemplates/edit.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blog:homepage')
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)


class Delete(DeleteView):
    model = Post
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blog:homepage')
    template_name = 'blogtemplates/confirm-delete.html'
        
        
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)




