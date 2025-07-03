from django.contrib import admin
from . import models

# Register your models here.

class AuthorAdmin( admin.ModelAdmin ):
    list_display = ('title','status' ,'author')
    fields = ('title', 'slug', 'author', 'publish', 'excerpt', 'content', 'status')
    readonly_fields = ('slug',)
admin.site.register(models.Post, AuthorAdmin)