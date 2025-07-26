from django.contrib import admin
from . import models

# Register your models here.
 
class AuthorAdmin( admin.ModelAdmin ):
    list_display = ('title','id','status' ,'author')
    fields = ('title', 'slug', 'image', 'author', 'publish', 'excerpt', 'content', 'status')
    readonly_fields = ('slug',)
admin.site.register(models.Post, AuthorAdmin)



@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email',  'publish', 'status')
    list_filter = ('status', 'publish')
    search_fields = ('name', 'email', 'content')
