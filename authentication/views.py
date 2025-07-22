from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django_otp.decorators import otp_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.util import random_hex
import qrcode
import io
import base64
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailVerification, PasswordResetToken, GoogleAuth
import json


def custom_login(request):
    """Custom login view with 2FA support and email verification"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # First step: authenticate username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user account is active
            if not user.is_active:
                # Check if they just need email verification
                if not hasattr(user, 'email_verifications') or not user.email_verifications.filter(is_verified=True).exists():
                    messages.error(request, 'Your email address is not verified. Please check your email for the verification link or request a new one.')
                    return render(request, 'authentication/login.html', {'show_resend_verification': True, 'email': user.email})
                else:
                    messages.error(request, 'Your account is inactive. Please contact support.')
                    return render(request, 'authentication/login.html')
            
            # Double-check email verification for active users (belt and suspenders)
            if not hasattr(user, 'email_verifications') or not user.email_verifications.filter(is_verified=True).exists():
                messages.error(request, 'Your email address is not verified. Please check your email for the verification link.')
                return render(request, 'authentication/login.html', {'show_resend_verification': True, 'email': user.email})
            
            # Check if user has 2FA enabled
            if user.totpdevice_set.filter(confirmed=True).exists():
                # Store user in session for 2FA verification
                request.session['pre_2fa_user_id'] = user.id
                return redirect('authentication:two_factor_verify')
            else:
                # No 2FA, login directly
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')


def two_factor_verify(request):
    """2FA verification step"""
    if 'pre_2fa_user_id' not in request.session:
        messages.error(request, 'Please log in first.')
        return redirect('authentication:login')
    
    user_id = request.session['pre_2fa_user_id']
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('authentication:login')
    
    if request.method == 'POST':
        token = request.POST.get('token')
        
        # Check TOTP devices
        for device in user.totpdevice_set.filter(confirmed=True):
            if device.verify_token(token):
                # Valid token, complete login
                login(request, user)
                del request.session['pre_2fa_user_id']
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
        
        # Check static backup tokens
        for device in user.staticdevice_set.all():
            if device.verify_token(token):
                login(request, user)
                del request.session['pre_2fa_user_id']
                messages.success(request, f'Welcome back, {user.first_name or user.username}! (Backup token used)')
                return redirect('dashboard')
        
        messages.error(request, 'Invalid authentication code.')
    
    return render(request, 'authentication/two_factor_verify.html', {'user': user})


@login_required
def two_factor_setup(request):
    """Setup 2FA for user account"""
    user = request.user
    
    # Check if user already has 2FA enabled
    existing_device = user.totpdevice_set.filter(confirmed=True).first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'enable':
            # Create new TOTP device
            device = TOTPDevice.objects.create(
                user=user,
                name='Authenticator App',
                confirmed=False
            )
            
            # Generate QR code
            qr_url = device.config_url
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            qr_code_data = base64.b64encode(buffer.getvalue()).decode()
            
            return render(request, 'authentication/setup_2fa.html', {
                'device': device,
                'qr_code': qr_code_data,
                'secret_key': device.bin_key.hex(),
                'step': 'configure'
            })
        
        elif action == 'confirm':
            device_id = request.POST.get('device_id')
            token = request.POST.get('token')
            
            try:
                device = TOTPDevice.objects.get(id=device_id, user=user, confirmed=False)
                if device.verify_token(token):
                    device.confirmed = True
                    device.save()
                    
                    # Generate backup tokens
                    static_device = StaticDevice.objects.create(user=user, name='Backup Tokens')
                    backup_tokens = []
                    for _ in range(10):
                        token = StaticToken.random_token()
                        StaticToken.objects.create(device=static_device, token=token)
                        backup_tokens.append(token)
                    
                    messages.success(request, '2FA has been enabled successfully!')
                    return render(request, 'authentication/backup_tokens.html', {
                        'backup_tokens': backup_tokens
                    })
                else:
                    messages.error(request, 'Invalid verification code. Please try again.')
                    return redirect('authentication:two_factor_setup')
            except TOTPDevice.DoesNotExist:
                messages.error(request, 'Invalid setup session.')
                return redirect('authentication:two_factor_setup')
        
        elif action == 'disable':
            # Disable 2FA
            user.totpdevice_set.all().delete()
            user.staticdevice_set.all().delete()
            messages.success(request, '2FA has been disabled.')
            return redirect('authentication:two_factor_setup')
    
    return render(request, 'authentication/setup_2fa.html', {
        'existing_device': existing_device,
        'step': 'initial'
    })


@login_required
def backup_tokens(request):
    """View and regenerate backup tokens"""
    user = request.user
    static_devices = user.staticdevice_set.all()
    
    if request.method == 'POST' and request.POST.get('action') == 'regenerate':
        # Delete existing tokens and generate new ones
        for device in static_devices:
            device.token_set.all().delete()
        
        if static_devices.exists():
            static_device = static_devices.first()
        else:
            static_device = StaticDevice.objects.create(user=user, name='Backup Tokens')
        
        backup_tokens = []
        for _ in range(10):
            token = StaticToken.random_token()
            StaticToken.objects.create(device=static_device, token=token)
            backup_tokens.append(token)
        
        messages.success(request, 'New backup tokens generated!')
        return render(request, 'authentication/backup_tokens.html', {
            'backup_tokens': backup_tokens,
            'regenerated': True
        })
    
    # Get unused tokens
    unused_tokens = []
    for device in static_devices:
        unused_tokens.extend([token.token for token in device.token_set.all()])
    
    return render(request, 'authentication/backup_tokens.html', {
        'unused_tokens': unused_tokens
    })


def custom_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


@login_required
def security_settings(request):
    """Security settings page"""
    user = request.user
    has_2fa = user.totpdevice_set.filter(confirmed=True).exists()
    
    context = {
        'has_2fa': has_2fa,
        'login_sessions': []  # You can implement session tracking here
    }
    
    return render(request, 'authentication/security_settings.html', context)


def send_verification_email(request):
    """Send email verification link"""
    email = request.GET.get('email', '')  # Pre-fill from URL parameter
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Create email verification record
            verification = EmailVerification.objects.create(
                user=user,
                email=email
            )
            
            # Send verification email
            verification_url = request.build_absolute_uri(
                reverse('authentication:verify_email', args=[verification.token])
            )
            
            subject = 'Verify Your Email - Kwa Stage Boda Boda Welfare'
            message = f"""
Hello {user.first_name or user.username},

Please click the link below to verify your email address:
{verification_url}

This link will expire in 24 hours.

If you didn't request this verification, please ignore this email.

Best regards,
Kwa Stage Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f'Verification email sent to {email}. Please check your inbox.')
            return redirect('authentication:login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
        except Exception as e:
            messages.error(request, 'Failed to send verification email. Please try again.')
    
    return render(request, 'authentication/send_verification.html', {'email': email})


def verify_email(request, token):
    """Verify email address"""
    try:
        verification = EmailVerification.objects.get(token=token)
        
        if verification.is_expired():
            messages.error(request, 'Verification link has expired. Please request a new one.')
            return redirect('authentication:send_verification')
        
        if verification.is_verified:
            messages.info(request, 'Email already verified.')
            return redirect('authentication:login')
        
        # Mark as verified
        verification.is_verified = True
        verification.save()
        
        # Activate user account if not active
        user = verification.user
        if not user.is_active:
            user.is_active = True
            user.save()
        
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('authentication:login')
        
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('authentication:send_verification')


def forgot_password(request):
    """Send password reset email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Create password reset token
            reset_token = PasswordResetToken.objects.create(user=user)
            
            # Send reset email
            reset_url = request.build_absolute_uri(
                reverse('authentication:reset_password', args=[reset_token.token])
            )
            
            subject = 'Password Reset - Boda Boda Welfare System'
            message = f"""
Hello {user.first_name or user.username},

You requested a password reset. Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Boda Boda Welfare System Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f'Password reset email sent to {email}')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
        except Exception as e:
            messages.error(request, 'Failed to send reset email. Please try again.')
    
    return render(request, 'authentication/forgot_password.html')


def reset_password(request, token):
    """Reset password using token"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if reset_token.is_expired() or reset_token.is_used:
            messages.error(request, 'Reset link has expired or already been used. Please request a new one.')
            return redirect('authentication:forgot_password')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'authentication/reset_password.html', {'token': token})
            
            # Update password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('authentication:login')
        
        return render(request, 'authentication/reset_password.html', {'token': token})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('authentication:forgot_password')


def generate_qr_code(request):
    """Generate QR code for user registration or info"""
    if request.method == 'POST':
        data = request.POST.get('data', '')
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return JsonResponse({
            'qr_code': f'data:image/png;base64,{img_str}',
            'success': True
        })
    
    return render(request, 'authentication/generate_qr.html')


def google_signin(request):
    """Handle Google Sign-In authentication"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            credential = data.get('credential')
            
            # Here you would verify the Google JWT token
            # For demonstration, we'll create a placeholder response
            
            # In a real implementation, you would:
            # 1. Verify the JWT token with Google
            # 2. Extract user information
            # 3. Create or get the user account
            # 4. Log them in
            
            return JsonResponse({
                'success': False,
                'error': 'Google Sign-In requires proper OAuth2 configuration. Please contact the administrator.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Authentication failed'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
