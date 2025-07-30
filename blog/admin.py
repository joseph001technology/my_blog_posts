from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


# Register your models here.
 
class AuthorAdmin( admin.ModelAdmin ):
    list_display = ('title','id','status' ,'author')
    fields = ('title', 'slug', 'image', 'author', 'published_at', 'excerpt', 'content', 'status')
    readonly_fields = ('slug',)
admin.site.register(models.Post, AuthorAdmin)


admin.site.register(models.Comment, MPTTModelAdmin)
