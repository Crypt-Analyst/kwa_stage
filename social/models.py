from django.db import models
from django.contrib.auth.models import User
from members.models import Member
from stages.models import Stage

class Post(models.Model):
    """
    Social media posts by members
    """
    POST_TYPES = [
        ('text', 'Text Post'),
        ('photo', 'Photo Post'),
        ('emergency', 'Emergency Alert'),
        ('announcement', 'Announcement'),
        ('safety_tip', 'Safety Tip'),
    ]
    
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='text')
    image = models.ImageField(upload_to='social_posts/', blank=True, null=True)
    
    # Location and targeting
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True, 
                             help_text="Target specific stage (leave blank for all)")
    location = models.CharField(max_length=200, blank=True, help_text="Current location when posting")
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.user.get_full_name()}: {self.content[:50]}..."

class PostLike(models.Model):
    """
    Likes on posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')

class Comment(models.Model):
    """
    Comments on posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, 
                              related_name='replies')
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

class CommentLike(models.Model):
    """
    Likes on comments
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')

class Friendship(models.Model):
    """
    Friend connections between members
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
    ]
    
    requester = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('requester', 'receiver')
    
    def __str__(self):
        return f"{self.requester} -> {self.receiver} ({self.status})"

class GroupChat(models.Model):
    """
    Group chats for different stages
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='group_chats')
    admins = models.ManyToManyField(Member, related_name='admin_groups')
    members = models.ManyToManyField(Member, related_name='group_memberships')
    
    # Settings
    is_private = models.BooleanField(default=False)
    allow_all_members = models.BooleanField(default=True, help_text="Allow all stage members to join")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.stage.name})"

class ChatMessage(models.Model):
    """
    Messages in group chats
    """
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('location', 'Location'),
        ('emergency', 'Emergency Alert'),
    ]
    
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    
    # Location data for location sharing
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    
    # Message status
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

class MessageRead(models.Model):
    """
    Track which messages have been read by which users
    """
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='read_receipts')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')

class StageStory(models.Model):
    """
    Stories/updates from different stages (like Instagram stories)
    """
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='stories')
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='stage_stories/', blank=True, null=True)
    
    # Story expires after 24 hours
    expires_at = models.DateTimeField()
    
    # Engagement
    views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Stage Stories"

class StoryView(models.Model):
    """
    Track who has viewed which stories
    """
    story = models.ForeignKey(StageStory, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(Member, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'viewer')

class SocialNotification(models.Model):
    """
    Notifications for social interactions
    """
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
        ('friend_accepted', 'Friend Accepted'),
        ('mention', 'Mention'),
        ('group_invite', 'Group Invite'),
        ('story_view', 'Story View'),
    ]
    
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='social_notifications')
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sent_social_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Related objects
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, blank=True, null=True)
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
