from django.contrib import admin
from .models import Post, Comment, Hashtag

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'content', 'created_at', 'updated_at',]
    list_display_links = ['id', 'post_id']

@admin.register(Hashtag)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'hashtag_content']
    list_display_links = ['id', 'hashtag_content']