"""
Middleware to track user online status and activity.
"""

from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from members.models import Member


class OnlineStatusMiddleware:
    """
    Middleware to track when users are online and update their activity.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update user's online status if they're authenticated
        if not isinstance(request.user, AnonymousUser) and hasattr(request.user, 'member'):
            try:
                member = request.user.member
                Member.objects.filter(id=member.id).update(
                    is_online=True,
                    last_activity=timezone.now(),
                    last_seen=timezone.now()
                )
            except Member.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
