from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name', 'first_name')
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

admin.site.register(User, UserAdminConfig)


 
 
class AuthorAdmin( admin.ModelAdmin ):
    list_display = ('title','id','status' ,'author')
    fields = ('title', 'slug', 'image', 'author', 'published_at', 'excerpt', 'content', 'status')
    readonly_fields = ('slug',)
admin.site.register(models.Post, AuthorAdmin)


admin.site.register(models.Comment, MPTTModelAdmin)
