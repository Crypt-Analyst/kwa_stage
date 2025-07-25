"""
Django signals for the social app.
Auto-add members to stage group chats when they join.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from members.models import Member
from .models import GroupChat


@receiver(post_save, sender=Member)
def add_member_to_stage_group(sender, instance, created, **kwargs):
    """
    Automatically add new members to their stage's main group chat.
    """
    if created and instance.stage:
        try:
            # Get or create the stage's main group chat
            stage_group, group_created = GroupChat.objects.get_or_create(
                stage=instance.stage,
                name=f"{instance.stage.name} Main Chat",
                defaults={
                    'description': f"Main group chat for {instance.stage.name} stage members",
                    'allow_all_members': True,
                    'created_by': instance,
                    'is_private': False,
                }
            )
            
            # Add the new member to the group
            stage_group.members.add(instance)
            
            # If this is the first member, add them as admin
            if stage_group.members.count() == 1:
                stage_group.admins.add(instance)
                
        except Exception as e:
            # Log error but don't break member creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to add member {instance.id} to stage group: {e}")


@receiver(post_save, sender=Member)
def update_member_activity(sender, instance, **kwargs):
    """
    Update member's last activity when their record is saved.
    """
    if not kwargs.get('created', False):
        # Update last activity for existing members
        Member.objects.filter(id=instance.id).update(
            last_activity=instance.updated_at
        )
