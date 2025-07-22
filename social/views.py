from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from members.models import Member
from stages.models import Stage
from .models import (
    Post, PostLike, Comment, CommentLike, Friendship, 
    GroupChat, ChatMessage, MessageRead, StageStory, 
    StoryView, SocialNotification
)
from .forms import PostForm, CommentForm, GroupChatForm, ChatMessageForm
import json

@login_required
def feed(request):
    """
    Main social feed - shows posts from friends and same stage
    """
    try:
        member = request.user.member
        
        # Get posts from friends and same stage
        friends = Friendship.objects.filter(
            Q(requester=member) | Q(receiver=member),
            status='accepted'
        ).values_list('requester', 'receiver')
        
        friend_ids = set()
        for req, rec in friends:
            friend_ids.add(req if req != member.id else rec)
        
        # Posts from friends, same stage, or public announcements
        posts = Post.objects.filter(
            Q(author__in=friend_ids) |  # Friends' posts
            Q(stage=member.stage) |     # Same stage posts
            Q(stage__isnull=True) |     # Public posts
            Q(post_type='announcement') # All announcements
        ).select_related('author__user', 'stage').prefetch_related('likes', 'comments')
        
        # Handle new post submission
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = member
                post.save()
                messages.success(request, "Post shared successfully!")
                return redirect('social:feed')
        else:
            form = PostForm()
        
        # Pagination
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        
        # Get active stories
        stories = StageStory.objects.filter(
            expires_at__gt=timezone.now(),
            stage=member.stage
        ).select_related('author__user', 'stage')
        
        # Get friend suggestions
        existing_friends = friend_ids
        existing_friends.add(member.id)
        
        friend_suggestions = Member.objects.filter(
            stage=member.stage,
            status='active'
        ).exclude(id__in=existing_friends)[:5]
        
        context = {
            'posts': page_posts,
            'form': form,
            'stories': stories,
            'friend_suggestions': friend_suggestions,
            'member': member,
        }
        
        # Return modal-friendly content for AJAX requests
        if request.GET.get('modal') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'social/modal_feed.html', context)
        
        return render(request, 'social/feed.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')

@login_required
def like_post(request, post_id):
    """
    AJAX endpoint to like/unlike a post
    """
    if request.method == 'POST':
        try:
            member = request.user.member
            post = get_object_or_404(Post, id=post_id)
            
            like, created = PostLike.objects.get_or_create(
                post=post, 
                user=member
            )
            
            if not created:
                like.delete()
                liked = False
                post.likes_count = max(0, post.likes_count - 1)
            else:
                liked = True
                post.likes_count += 1
                
                # Create notification for post author
                if post.author != member:
                    SocialNotification.objects.create(
                        recipient=post.author,
                        sender=member,
                        notification_type='like',
                        post=post,
                        message=f"{member.user.get_full_name()} liked your post"
                    )
            
            post.save()
            
            return JsonResponse({
                'liked': liked,
                'likes_count': post.likes_count
            })
            
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member profile required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST required'}, status=405)

@login_required
def add_comment(request, post_id):
    """
    Add a comment to a post
    """
    if request.method == 'POST':
        try:
            member = request.user.member
            post = get_object_or_404(Post, id=post_id)
            
            content = request.POST.get('content', '').strip()
            if not content:
                return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
            
            comment = Comment.objects.create(
                post=post,
                author=member,
                content=content
            )
            
            # Update post comment count
            post.comments_count += 1
            post.save()
            
            # Create notification for post author
            if post.author != member:
                SocialNotification.objects.create(
                    recipient=post.author,
                    sender=member,
                    notification_type='comment',
                    post=post,
                    comment=comment,
                    message=f"{member.user.get_full_name()} commented on your post"
                )
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.user.get_full_name(),
                    'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
                },
                'comments_count': post.comments_count
            })
            
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member profile required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST required'}, status=405)

@login_required
def friends(request):
    """
    Friends management page
    """
    try:
        member = request.user.member
        
        # Get current friends
        friendships = Friendship.objects.filter(
            Q(requester=member) | Q(receiver=member),
            status='accepted'
        ).select_related('requester__user', 'receiver__user', 'requester__stage', 'receiver__stage')
        
        friends = []
        for friendship in friendships:
            friend = friendship.receiver if friendship.requester == member else friendship.requester
            friends.append(friend)
        
        # Get pending friend requests (received)
        pending_requests = Friendship.objects.filter(
            receiver=member,
            status='pending'
        ).select_related('requester__user', 'requester__stage')
        
        # Get sent requests
        sent_requests = Friendship.objects.filter(
            requester=member,
            status='pending'
        ).select_related('receiver__user', 'receiver__stage')
        
        # Get friend suggestions (same stage, not already friends)
        existing_connections = set()
        for friendship in Friendship.objects.filter(
            Q(requester=member) | Q(receiver=member)
        ):
            if friendship.requester == member:
                existing_connections.add(friendship.receiver.id)
            else:
                existing_connections.add(friendship.requester.id)
        
        existing_connections.add(member.id)
        
        suggested_friends = Member.objects.filter(
            stage=member.stage,
            status='active'
        ).exclude(id__in=existing_connections).select_related('user', 'stage')[:10]
        
        # Get online friends (mock for now)
        online_friends = friends[:5]  # Mock implementation
        
        # Get available members for creating chats
        available_members = Member.objects.filter(
            status='active'
        ).exclude(id=member.id).select_related('user', 'stage')[:20]
        
        context = {
            'friends': friends,
            'friends_count': len(friends),
            'pending_requests': pending_requests,
            'sent_requests': sent_requests,
            'suggested_friends': suggested_friends,
            'online_friends': online_friends,
            'available_members': available_members,
            'member': member,
        }
        
        # Handle modal requests
        if request.GET.get('modal') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'social/modal_friends.html', context)
        
        return render(request, 'social/friends.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')

@login_required
def send_friend_request(request, member_id):
    """
    Send a friend request
    """
    if request.method == 'POST':
        try:
            sender = request.user.member
            receiver = get_object_or_404(Member, id=member_id)
            
            if sender == receiver:
                return JsonResponse({'error': 'Cannot send friend request to yourself'}, status=400)
            
            # Check if friendship already exists
            existing = Friendship.objects.filter(
                Q(requester=sender, receiver=receiver) |
                Q(requester=receiver, receiver=sender)
            ).first()
            
            if existing:
                return JsonResponse({'error': 'Friendship request already exists'}, status=400)
            
            # Create friend request
            friendship = Friendship.objects.create(
                requester=sender,
                receiver=receiver
            )
            
            # Create notification
            SocialNotification.objects.create(
                recipient=receiver,
                sender=sender,
                notification_type='friend_request',
                message=f"{sender.user.get_full_name()} sent you a friend request"
            )
            
            return JsonResponse({'success': True, 'message': 'Friend request sent!'})
            
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member profile required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST required'}, status=405)

@login_required
def accept_friend_request(request, friendship_id):
    """
    Accept a friend request
    """
    if request.method == 'POST':
        try:
            member = request.user.member
            friendship = get_object_or_404(
                Friendship, 
                id=friendship_id, 
                receiver=member, 
                status='pending'
            )
            
            friendship.status = 'accepted'
            friendship.save()
            
            # Create notification for requester
            SocialNotification.objects.create(
                recipient=friendship.requester,
                sender=member,
                notification_type='friend_accepted',
                message=f"{member.user.get_full_name()} accepted your friend request"
            )
            
            return JsonResponse({'success': True, 'message': 'Friend request accepted!'})
            
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member profile required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST required'}, status=405)

@login_required
def group_chats(request):
    """
    Group chats management
    """
    try:
        member = request.user.member
        
        # Get member's group chats
        group_chats = GroupChat.objects.filter(
            Q(members=member) | Q(stage=member.stage, allow_all_members=True)
        ).distinct().select_related('stage', 'created_by__user').prefetch_related('members')
        
        # Get direct messages (conversations between two people)
        direct_chats = GroupChat.objects.filter(
            members=member,
            is_direct=True
        ).distinct().select_related('created_by__user').prefetch_related('members')
        
        # Add last message and unread count to each chat
        for chat in group_chats:
            chat.last_message = chat.messages.filter(is_deleted=False).order_by('-created_at').first()
            chat.unread_count = chat.messages.filter(
                is_deleted=False
            ).exclude(read_receipts__user=member).count()
        
        for chat in direct_chats:
            chat.last_message = chat.messages.filter(is_deleted=False).order_by('-created_at').first()
            chat.unread_count = chat.messages.filter(
                is_deleted=False
            ).exclude(read_receipts__user=member).count()
            
            # Get the other member for direct chats
            other_members = chat.members.exclude(id=member.id)
            chat.other_member = other_members.first() if other_members.exists() else None
        
        # Get stage's default group
        stage_group, created = GroupChat.objects.get_or_create(
            stage=member.stage,
            name=f"{member.stage.name} Main Chat",
            defaults={
                'description': f"Main group chat for {member.stage.name} stage",
                'allow_all_members': True
            }
        )
        
        if created or member not in stage_group.members.all():
            stage_group.members.add(member)
            
        # Get available members for creating chats
        available_members = Member.objects.filter(
            status='active'
        ).exclude(id=member.id).select_related('user', 'stage')[:20]

        context = {
            'group_chats': group_chats,
            'direct_chats': direct_chats,
            'available_members': available_members,
            'stage_group': stage_group,
            'member': member,
        }
        
        # Handle modal requests
        if request.GET.get('modal') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'social/modal_chat.html', context)
        
        return render(request, 'social/group_chats.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')

@login_required
def chat_detail(request, chat_id):
    """
    Individual chat view with messages
    """
    try:
        member = request.user.member
        chat = get_object_or_404(GroupChat, id=chat_id)
        
        # Check if member has access to this chat
        has_access = (
            member in chat.members.all() or 
            (chat.stage == member.stage and chat.allow_all_members)
        )
        
        if not has_access:
            messages.error(request, "You don't have access to this chat.")
            return redirect('social:group_chats')
        
        # Get messages
        messages_list = chat.messages.filter(
            is_deleted=False
        ).select_related('sender__user')
        
        # Handle new message
        if request.method == 'POST':
            content = request.POST.get('content', '').strip()
            if content:
                message = ChatMessage.objects.create(
                    group=chat,
                    sender=member,
                    content=content
                )
                
                # Mark as read by sender
                MessageRead.objects.create(
                    message=message,
                    user=member
                )
                
                return redirect('social:chat_detail', chat_id=chat.id)
        
        # Mark messages as read
        unread_messages = messages_list.exclude(
            read_receipts__user=member
        )
        for message in unread_messages:
            MessageRead.objects.get_or_create(
                message=message,
                user=member
            )
        
        context = {
            'chat': chat,
            'messages': messages_list,
            'member': member,
        }
        
        return render(request, 'social/chat_detail.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')

@login_required
def notifications(request):
    """
    Social notifications page
    """
    try:
        member = request.user.member
        
        # Get notifications
        notifications_list = member.social_notifications.all().select_related(
            'sender__user', 'post', 'comment', 'group'
        ).order_by('-created_at')
        
        # Mark as read if requested
        if request.GET.get('mark_read'):
            notifications_list.update(is_read=True)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('social:notifications')
        
        # Pagination
        paginator = Paginator(notifications_list, 20)
        page_number = request.GET.get('page')
        page_notifications = paginator.get_page(page_number)
        
        context = {
            'notifications': page_notifications,
            'unread_count': notifications_list.filter(is_read=False).count(),
            'member': member,
        }
        
        # Handle modal requests
        if request.GET.get('modal') == '1' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'social/modal_notifications.html', context)
        
        return render(request, 'social/notifications.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')

@login_required
def stories(request):
    """
    Stage stories view
    """
    try:
        member = request.user.member
        
        # Get active stories for member's stage
        active_stories = StageStory.objects.filter(
            stage=member.stage,
            expires_at__gt=timezone.now()
        ).select_related('author__user')
        
        # Handle new story creation
        if request.method == 'POST':
            content = request.POST.get('content', '')
            image = request.FILES.get('image')
            
            if content or image:
                story = StageStory.objects.create(
                    stage=member.stage,
                    author=member,
                    content=content,
                    image=image,
                    expires_at=timezone.now() + timedelta(hours=24)
                )
                messages.success(request, "Story shared successfully!")
                return redirect('social:stories')
        
        context = {
            'stories': active_stories,
            'member': member,
        }
        
        return render(request, 'social/stories.html', context)
        
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')
