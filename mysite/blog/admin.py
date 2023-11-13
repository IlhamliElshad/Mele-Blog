from .models import Post, Comment
from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','author', 'publish', 'status']
    list_filter = ['status']
    search_fields = ['title', 'body']
    date_hierarchy = 'publish'
    ordering = ['created']
    prepopulated_fields = {"slug": ('title',)}
    raw_id_fields = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
