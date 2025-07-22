from django import forms
from .models import Post, Comment, GroupChat, ChatMessage, StageStory

class PostForm(forms.ModelForm):
    """
    Form for creating social posts
    """
    class Meta:
        model = Post
        fields = ['content', 'post_type', 'image', 'stage', 'location']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "What's happening in your stage today?",
                'required': True
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'stage': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current location (optional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user_member = kwargs.pop('user_member', None)
        super().__init__(*args, **kwargs)
        
        # Set stage choices based on user's access
        if user_member:
            from stages.models import Stage
            stage_choices = [('', 'All Stages (Public)')]
            stage_choices.append((user_member.stage.id, user_member.stage.name))
            
            self.fields['stage'].choices = stage_choices
        
        # Make stage optional for public posts
        self.fields['stage'].required = False

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to posts
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write a comment...',
                'required': True
            })
        }

class GroupChatForm(forms.ModelForm):
    """
    Form for creating group chats
    """
    class Meta:
        model = GroupChat
        fields = ['name', 'description', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Chat group name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this group chat...'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class ChatMessageForm(forms.ModelForm):
    """
    Form for sending chat messages
    """
    class Meta:
        model = ChatMessage
        fields = ['content', 'message_type', 'image']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message...',
                'autocomplete': 'off'
            }),
            'message_type': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'display: none;'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_type'].initial = 'text'

class StageStoryForm(forms.ModelForm):
    """
    Form for creating stage stories
    """
    class Meta:
        model = StageStory
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Share what's happening at your stage...",
                'maxlength': 500
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class SearchForm(forms.Form):
    """
    Form for searching posts and members
    """
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts, members, or stages...',
            'autocomplete': 'off'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('posts', 'Posts'),
            ('members', 'Members'),
            ('groups', 'Group Chats')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        initial='all'
    )
