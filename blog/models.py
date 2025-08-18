from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import NewManager
from .constants import CHOICES, DRAFT
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image

User = get_user_model()

def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)


class Post(models.Model):
    objects = models.Manager()  # Default manager
    published = NewManager()

    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True, blank=True, verbose_name="Excerpt (optional)")
    image = models.ImageField(upload_to=user_directory_path, default='posts/default.png', blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published_at', blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=CHOICES, default=DRAFT)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)
    newmanager = NewManager()

    def save(self, *args, **kwargs):
        # Save first to get an ID for upload path
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            with Image.open(img_path) as img:
                # Force resize to exactly 500x800 (stretch/compress)
                img = img.resize((1200, 800), Image.Resampling.LANCZOS)
                img.save(img_path)

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    email = models.EmailField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['published_at']

    def __str__(self):
        return f'Comment by {self.name}'




class Vote(models.Model):

    post = models.ForeignKey(Post, related_name='postid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('post', 'user')  # Each user can vote once per post