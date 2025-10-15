
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import transaction, IntegrityError
from .models import Post
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.conf import settings

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

# def assign_user_group(sender, instance, created, **kwargs):
#     # Ensure groups exist
#     privileged_group, _ = Group.objects.get_or_create(name="Privileged")
#     default_group, _ = Group.objects.get_or_create(name="Default")

#     if created:
#         if instance.user_name == "josephkiarie" or instance.is_superuser:
#             instance.groups.add(privileged_group)
#         else:
#             instance.groups.add(default_group)
#         instance.save()
        
        
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.clear()
        group = Group.objects.filter(name__iexact=instance.role).first()

        if group:
            instance.groups.add(group)
            instance.save()
        else:
            print(f"⚠️ No group found for role '{instance.role}' — user {instance.user_name} not assigned.")
   