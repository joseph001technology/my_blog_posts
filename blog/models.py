from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import NewManager
from .constants import  CHOICES,DRAFT



User = get_user_model()

# Create your models here.
class Post(models.Model) :#database table
    objects = models.Manager()  # Default manager
    published = NewManager()
# Table columns

    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True,blank=True,verbose_name="Excerpt (optional)")
    slug = models.SlugField(max_length=250, unique_for_date='publish',blank=True )
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=CHOICES, default=DRAFT)
    objects = models.Manager()  # default manager
    newmanager = NewManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title



# Create your models here.
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    
    class Meta:
            ordering = ('publish',)

    def __str__(self):
            return f'Comment by {self.name}'
    
    