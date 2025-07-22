from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    # Main social feed
    path('', views.feed, name='feed'),
    
    # Post interactions
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # Friends management
    path('friends/', views.friends, name='friends'),
    path('friends/request/<int:member_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/accept/<int:friendship_id>/', views.accept_friend_request, name='accept_friend_request'),
    
    # Group chats
    path('chats/', views.group_chats, name='group_chats'),
    path('chats/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Stories
    path('stories/', views.stories, name='stories'),
]
