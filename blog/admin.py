from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'heading', 'is_published']
    readonly_fields = ['author', 'text', 'heading', 'short_definition', 'pub_date', 'is_published']
    search_fields = ['author__username', 'heading']
    date_hierarchy = 'pub_date'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'is_published']
    readonly_fields = ['author', 'text', 'post']
    search_fields = ['author__username']
    date_hierarchy = 'pub_date'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
