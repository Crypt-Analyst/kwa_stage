from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django_otp import user_has_device
from django.conf import settings


class TwoFactorMiddleware:
    """
    Middleware that enforces 2FA for sensitive operations and URLs.
    Automatically redirects users to enable 2FA if accessing protected resources.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that require 2FA (can be configured in settings)
        self.protected_urls = getattr(settings, 'TWO_FA_REQUIRED_URLS', [
            '/contributions/make-payment/',
            '/contributions/mpesa/',
            '/emergency/report-case/',
            '/loans/apply/',
            '/loans/approve/',
            '/admin/',
            '/settings/',
        ])
        
        # URL patterns that are always exempt from 2FA
        self.exempt_urls = [
            '/auth/',
            '/login/',
            '/logout/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check if the requested view requires 2FA verification.
        """
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return None
        
        # Skip if view is marked as 2FA exempt
        if hasattr(view_func, '_two_fa_exempt'):
            return None
        
        # Skip exempt URLs
        if any(request.path.startswith(url) for url in self.exempt_urls):
            return None
        
        # Check if URL requires 2FA
        requires_2fa = any(request.path.startswith(url) for url in self.protected_urls)
        
        if requires_2fa:
            user = request.user
            
            # Check if user has 2FA enabled
            if not user_has_device(user):
                messages.warning(
                    request,
                    'Two-Factor Authentication is required to access this feature. Please enable 2FA first.'
                )
                return redirect('authentication:two_factor_setup')
            
            # Check if user is verified for this session
            if not user.is_verified():
                messages.warning(
                    request,
                    'Please verify your identity with 2FA to continue.'
                )
                # Store the intended URL to redirect after verification
                request.session['next_url'] = request.get_full_path()
                return redirect('authentication:two_factor_verify')
        
        return None
