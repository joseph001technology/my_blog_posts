from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

 


 
 
class AuthorAdmin( admin.ModelAdmin ):
    list_display = ('title','id','status' ,'author')
    fields = ('title', 'slug', 'image', 'author', 'published_at', 'excerpt', 'content', 'status')
    readonly_fields = ('slug',)
admin.site.register(models.Post, AuthorAdmin)


admin.site.register(models.Comment, MPTTModelAdmin)
