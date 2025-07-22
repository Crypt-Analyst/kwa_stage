from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django_otp.decorators import otp_required
from django_otp import user_has_device


def require_2fa(view_func):
    """
    Decorator that requires 2FA to be enabled and verified for sensitive operations.
    Use this for financial transactions, emergency cases, and admin functions.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        # Check if user has 2FA enabled
        if not user_has_device(user):
            messages.warning(
                request, 
                'Two-Factor Authentication is required for this action. Please enable 2FA first.'
            )
            return redirect('authentication:two_factor_setup')
        
        # Check if user is verified for this session
        if not user.is_verified():
            messages.warning(
                request,
                'Please verify your identity with 2FA to access this feature.'
            )
            # Store the intended URL in session to redirect after verification
            request.session['next_url'] = request.get_full_path()
            return redirect('authentication:two_factor_verify')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def sensitive_operation(view_func):
    """
    Decorator for highly sensitive operations that always require 2FA verification,
    even within the same session. Use for: financial transfers, emergency fund access,
    user data changes, system settings.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        # Always require 2FA for sensitive operations
        if not user_has_device(user):
            messages.error(
                request,
                'Two-Factor Authentication is mandatory for this operation. Please enable 2FA.'
            )
            return redirect('authentication:two_factor_setup')
        
        # Always require fresh verification for sensitive operations
        if not user.is_verified():
            messages.warning(
                request,
                'Please verify your identity to perform this sensitive operation.'
            )
            request.session['next_url'] = request.get_full_path()
            return redirect('authentication:two_factor_verify')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def two_fa_exempt(view_func):
    """
    Decorator to mark views that don't require 2FA.
    Use for public pages, basic profile viewing, non-sensitive operations.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    wrapper._two_fa_exempt = True
    return wrapper
