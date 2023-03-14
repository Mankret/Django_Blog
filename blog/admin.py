from django.contrib import admin, messages
from django.utils.translation import ngettext

from blog.models import Comment, Post


# admin.site.register(Post)
# admin.site.register(Comment)


@admin.action(description='Mark selected posts as published')
def make_published_post(self, request, queryset):
    update = queryset.update(is_published=True)
    self.message_user(request, ngettext('%d post was successfully marked as published.',
                                        '%d posts were successfully marked as published.',
                                        update, ) % update, messages.SUCCESS)


@admin.action(description='Mark selected comments as published')
def make_published_comment(self, request, queryset):
    update = queryset.update(is_published=True)
    self.message_user(request, ngettext('%d comment was successfully marked as published.',
                                        '%d comments were successfully marked as published.',
                                        update, ) % update, messages.SUCCESS)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'is_posted', 'created_at']
    list_filter = ['author', 'is_published', 'created_at']
    list_display_links = ['author']

    search_fields = ['title', 'author']
    date_hierarchy = 'created_at'
    actions = [make_published_post]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at', 'is_published', 'post']
    list_filter = ['created_at', 'is_published']
    list_per_page = 10

    search_fields = ['text']
    date_hierarchy = 'created_at'
    list_select_related = ['post']
    actions = [make_published_comment]
    list_display_links = ['post']
