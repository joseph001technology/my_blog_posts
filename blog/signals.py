
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

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




 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)

 
        
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.clear()
        
        default_group, _ = Group.objects.get_or_create(name="Regular")
        privileged_group, _ = Group.objects.get_or_create(name="Privileged")

        instance.groups.add(default_group)

         
        instance.save()
        
    

        