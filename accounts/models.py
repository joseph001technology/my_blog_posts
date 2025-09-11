from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _



def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
def clean(self):
    if self.avatar and hasattr(self.avatar, "file"):
        w, h = get_image_dimensions(self.avatar)
        if w < 100 or h < 100:
            raise ValidationError(_("Avatar is too small. Minimum size is 100x100px."))
        if w > 1500 or h > 1500:
            raise ValidationError(_("Avatar is too large. Maximum size is 1500x1500px."))
     




    def __str__(self):
        return self.user.username
    
    
    
@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
