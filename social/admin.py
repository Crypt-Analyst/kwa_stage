from django.contrib import admin
from .models import (
    Post, PostLike, Comment, CommentLike, Friendship, 
    GroupChat, ChatMessage, MessageRead, StageStory, 
    StoryView, SocialNotification
)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'post_type', 'stage', 'likes_count', 'created_at', 'is_approved']
    list_filter = ['post_type', 'is_approved', 'is_pinned', 'created_at', 'stage']
    search_fields = ['content', 'author__user__first_name', 'author__user__last_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['likes_count', 'comments_count', 'shares_count']
    actions = ['approve_posts', 'pin_posts', 'unpin_posts']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
    approve_posts.short_description = 'Approve selected posts'
    
    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)
    pin_posts.short_description = 'Pin selected posts'
    
    def unpin_posts(self, request, queryset):
        queryset.update(is_pinned=False)
    unpin_posts.short_description = 'Unpin selected posts'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'likes_count', 'created_at']
    list_filter = ['created_at', 'post__post_type']
    search_fields = ['content', 'author__user__first_name', 'author__user__last_name']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['requester', 'receiver', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['requester__user__first_name', 'requester__user__last_name', 
                    'receiver__user__first_name', 'receiver__user__last_name']
    date_hierarchy = 'created_at'

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'stage', 'is_private', 'allow_all_members', 'created_at']
    list_filter = ['is_private', 'allow_all_members', 'created_at', 'stage']
    search_fields = ['name', 'description', 'stage__name']
    filter_horizontal = ['admins', 'members']
    date_hierarchy = 'created_at'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['group', 'sender', 'content_preview', 'message_type', 'created_at', 'is_deleted']
    list_filter = ['message_type', 'is_deleted', 'created_at', 'group']
    search_fields = ['content', 'sender__user__first_name', 'sender__user__last_name']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(StageStory)
class StageStoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'stage', 'content_preview', 'views_count', 'created_at', 'expires_at']
    list_filter = ['created_at', 'expires_at', 'stage']
    search_fields = ['content', 'author__user__first_name', 'author__user__last_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['views_count']
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
        return "Image story"
    content_preview.short_description = 'Content'

@admin.register(SocialNotification)
class SocialNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'message', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__user__first_name', 'recipient__user__last_name',
                    'sender__user__first_name', 'sender__user__last_name', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark selected notifications as unread'

# Inline admin classes for related models
class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0
    readonly_fields = ['user', 'created_at']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'created_at']
    fields = ['author', 'content', 'created_at']

# Register simple models without custom admin
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(MessageRead)
admin.site.register(StoryView)
