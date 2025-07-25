"""
Context processors for bodaboda_welfare project.
"""

from django.conf import settings


def google_maps_api_key(request):
    """Add Google Maps API key to template context."""
    return {
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    }


def site_settings(request):
    """Add common site settings to template context."""
    return {
        'SITE_NAME': 'Boda Boda Family',
        'SITE_TAGLINE': 'Stage ni yetu, sauti ni yao — we just build the mic',
    }
