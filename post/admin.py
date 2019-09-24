from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'image', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['created_at', 'updated_at', 'text']
    ordering = ['-updated_at', '-created_at']
    raw_if_fields = ['author']

