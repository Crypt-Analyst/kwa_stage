"""
Management command to mark inactive users as offline.
Run this periodically (e.g., every 5 minutes) via cron job.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from members.models import Member


class Command(BaseCommand):
    help = 'Mark users as offline if they have been inactive for more than 5 minutes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--minutes',
            type=int,
            default=5,
            help='Minutes of inactivity before marking user as offline (default: 5)'
        )

    def handle(self, *args, **options):
        minutes = options['minutes']
        cutoff_time = timezone.now() - timedelta(minutes=minutes)
        
        # Find users who were online but haven't been active recently
        inactive_users = Member.objects.filter(
            is_online=True,
            last_activity__lt=cutoff_time
        )
        
        count = inactive_users.count()
        
        # Mark them as offline
        inactive_users.update(is_online=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully marked {count} users as offline '
                f'(inactive for more than {minutes} minutes)'
            )
        )
