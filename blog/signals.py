# yourapp/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import transaction, IntegrityError
from .models import Post

@receiver(pre_save, sender=Post)
def generate_unique_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        for i in range(1, 100):  # limit retries
            if not Post.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
                instance.slug = unique_slug
                break
            unique_slug = f"{base_slug}-{i}"
        else:
            raise ValueError("Could not generate unique slug after 100 attempts")
