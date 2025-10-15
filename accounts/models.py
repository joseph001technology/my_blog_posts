from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

         

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
     


    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.user_name




def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

         
        group_name = self.role.capitalize()  
        group, _ = Group.objects.get_or_create(name=group_name)

        if not self.groups.filter(name=group_name).exists(): 
            self.groups.clear() 
            self.groups.add(group)





def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user =  models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def clean(self):
        if self.avatar and hasattr(self.avatar, "file"):
            MIN_WIDTH, MIN_HEIGHT = get_image_dimensions(self.avatar)
            if MIN_WIDTH < 100 or MIN_HEIGHT < 100:
                raise ValidationError(_("Avatar is too small. Minimum size is 100x100px."))
            if MIN_WIDTH > 1500 or MIN_HEIGHT > 1500:
                raise ValidationError(_("Avatar is too large. Maximum size is 1500x1500px."))
        




    def __str__(self):
        return self.user.user_name
            
    
    

    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile if it doesn’t exist
        Profile.objects.create(user=instance)
    else:
        # Only update profile if it exists
        if hasattr(instance, "profile"):
            instance.profile.save()

    