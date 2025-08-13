from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from allauth.socialaccount.providers.google.views import oauth2_login
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import NewCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .forms import PostSearchForm



def test_func(self):
    user = self.request.user
    return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)



def home(request):
    all_posts = Post.newmanager.all()
    return render(request, 'blogtemplates/index.html', {'posts': all_posts})

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.username == "josephkiarie" or user.is_superuser)


def post_single(request, slug):   
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Favourite logic
    fav = False
    if request.user.is_authenticated:
        if post.favourites.filter(id=request.user.id).exists():
            fav = True

    # Comments
    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                user_comment = comment_form.save(commit=False)
                user_comment.post = post
                user_comment.name = request.user.username
                user_comment.email = request.user.email
                user_comment.save()

                return HttpResponseRedirect(reverse('blog:post_single', args=[post.slug]))
            else:
                return HttpResponseRedirect('/accounts/login/')
    else:
        comment_form = NewCommentForm()

    return render(request, 'blogtemplates/single.html', {
        'post': post,
        'comments': comments,
        'user_comment': user_comment,
        'comment_form': comment_form,
        'fav': fav,
        'allcomments': allcomments
    })


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




def post_search(request):
    form = PostSearchForm()
    q = ''
    results = []
    query = Q()
    
    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        
        if form.is_valid():
            q = form.cleaned_data['q']
            
            if q:
                query &= Q(title__icontains=q)
    
            results = Post.objects.filter(query)
            
    return render(request, 'blogtemplates/search.html', {
        'form': form,
        'q': q,
        'results': results
    })
