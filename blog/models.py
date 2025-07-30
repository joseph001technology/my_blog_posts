from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import NewManager
from .constants import  CHOICES,DRAFT



User = get_user_model()

# Create your models here.

def user_directory_path(instance, filename):
    return f'blog/comments/images/{filename}'



class Post(models.Model) : 
    
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True,blank=True,verbose_name="Excerpt (optional)")
    image = models.ImageField(upload_to=user_directory_path,default='posts/default.png',blank=True,null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish',blank=True )
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=CHOICES, default=DRAFT)
    objects = models.Manager()  # default manager
    newmanager = NewManager()
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'posts/default.png'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-published_at',)

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
    
    