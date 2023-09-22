from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status']
    search_fields = ['title','body']
    date_hierarchy = 'publish'
    ordering = ['created']
    prepopulated_fields = {"slug":('title',)}
    raw_id_fields = ['author']