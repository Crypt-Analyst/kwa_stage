from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from members.models import Member
from contributions.models import Contribution, WelfareAccount
from emergency.models import EmergencyCase
from accidents.models import AccidentReport
from loans.models import Loan, LoanKitty

def home(request):
    """
    Modern landing page with system overview and key features
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Public statistics for the landing page
    stats = {
        'total_members': Member.objects.filter(status='active').count(),
        'total_stages': Member.objects.values('stage').distinct().count(),
        'total_contributions': WelfareAccount.get_current_balance(),
        'active_loans': Loan.objects.filter(status__in=['disbursed', 'repaying']).count(),
        'bikes_registered': Member.objects.filter(bikes__isnull=False).distinct().count(),
        'emergency_cases_resolved': EmergencyCase.objects.filter(status='resolved').count(),
    }
    
    # Key features for the landing page
    features = [
        {
            'icon': 'fas fa-users',
            'title': 'Member Management',
            'description': 'Comprehensive member registration, profiles, and stage management for the Boda Boda community.',
            'color': 'primary'
        },
        {
            'icon': 'fas fa-piggy-bank',
            'title': 'Welfare Contributions',
            'description': 'Track weekly and monthly contributions to build a strong welfare fund for community support.',
            'color': 'success'
        },
        {
            'icon': 'fas fa-heart',
            'title': 'Emergency Support',
            'description': 'Immediate family support during emergencies and bereavement. Boda Boda is Family.',
            'color': 'danger'
        },
        {
            'icon': 'fas fa-motorcycle',
            'title': 'Bike Registry & Safety',
            'description': 'Register your bike, track ownership, and report accidents for community safety.',
            'color': 'warning'
        },
        {
            'icon': 'fas fa-search',
            'title': 'Lost Bike Tracking',
            'description': 'Report and search for lost motorcycles with photo uploads and community alerts.',
            'color': 'info'
        },
        {
            'icon': 'fas fa-money-bill-wave',
            'title': 'Loan Fund',
            'description': 'Access affordable loans from the community kitty to grow your business.',
            'color': 'secondary'
        },
    ]
    
    # Testimonials/Success stories
    testimonials = [
        {
            'name': 'John Kamau',
            'stage': 'Githurai Stage',
            'message': 'This system helped my family during a difficult time. Boda Boda truly is family.',
            'rating': 5
        },
        {
            'name': 'Mary Wanjiku',
            'stage': 'CBD Stage',
            'message': 'The loan fund helped me repair my bike and get back to work quickly.',
            'rating': 5
        },
        {
            'name': 'Peter Ochieng',
            'stage': 'Eastleigh Stage',
            'message': 'Lost bike tracking feature helped me find my motorcycle in just 2 days!',
            'rating': 5
        },
    ]
    
    context = {
        'stats': stats,
        'features': features,
        'testimonials': testimonials,
        'slogan': 'Stage ni yetu, sauti ni yao — we just build the mic',
    }
    return render(request, 'home.html', context)

def about(request):
    """
    About page with system information, history, and developer details
    """
    return render(request, 'about.html')

@login_required
def dashboard(request):
    """
    Main dashboard with sidebar - shows different content based on user role
    """
    try:
        member = request.user.member
    except Member.DoesNotExist:
        member = None
    
    # Dashboard statistics
    context = {
        'member': member,
        'total_members': Member.objects.filter(status='active').count(),
        'total_contributions': WelfareAccount.get_current_balance(),
        'loan_fund_balance': LoanKitty.get_current_balance(),
        'pending_emergencies': EmergencyCase.objects.filter(status='reported').count(),
        'recent_accidents': AccidentReport.objects.filter(status='reported').count(),
        
        # Recent activities
        'recent_contributions': Contribution.objects.filter(status='completed').order_by('-payment_date')[:5],
        'recent_emergencies': EmergencyCase.objects.order_by('-created_at')[:5],
        'recent_accidents': AccidentReport.objects.order_by('-created_at')[:3],
        
        # Member specific data
        'member_contributions': Contribution.objects.filter(member=member, status='completed').aggregate(
            total=Sum('amount')
        )['total'] if member else 0,
        'member_loans': Loan.objects.filter(member=member).order_by('-application_date')[:3] if member else [],
    }
    
    return render(request, 'dashboard.html', context)

def user_login(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')

def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def register(request):
    """
    New member registration with email verification and Turnstile protection
    """
    if request.method == 'POST':
        # Verify Turnstile first
        from authentication.turnstile import verify_turnstile, get_turnstile_site_key
        turnstile_result = verify_turnstile(request)
        if not turnstile_result['success']:
            if not turnstile_result.get('sandbox'):
                messages.error(request, 'Security verification failed. Please try again.')
                return render(request, 'auth/register.html', {
                    'turnstile_site_key': get_turnstile_site_key()
                })
        
        # Handle user registration
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/register.html', {
                'turnstile_site_key': get_turnstile_site_key()
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/register.html', {
                'turnstile_site_key': get_turnstile_site_key()
            })
        
        # Create user account (inactive until email is verified)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Account inactive until email verification
        )
        
        # Send verification email
        from authentication.models import EmailVerification
        from django.core.mail import send_mail
        from django.conf import settings
        import uuid
        
        # Create verification token
        verification = EmailVerification.objects.create(
            user=user,
            token=str(uuid.uuid4())
        )
        
        # Send verification email
        verification_url = request.build_absolute_uri(f'/auth/verify-email/{verification.token}/')
        
        subject = 'Verify Your Email - Kwa Stage Boda Boda Welfare'
        message = f"""
        Hello {first_name},
        
        Thank you for registering with Kwa Stage Boda Boda Welfare System.
        
        Please click the link below to verify your email address:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create this account, please ignore this email.
        
        Best regards,
        Kwa Stage Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 
                'Registration successful! Please check your email to verify your account before logging in.')
        except Exception as e:
            messages.error(request, 
                'Registration successful, but we could not send the verification email. Please contact support.')
        
        return redirect('authentication:login')
    
    from authentication.turnstile import get_turnstile_site_key
    return render(request, 'auth/register.html', {
        'turnstile_site_key': get_turnstile_site_key()
    })

@login_required
def analytics(request):
    """Analytics view"""
    return render(request, 'analytics.html')

@login_required
@login_required
def settings(request):
    """System settings view"""
    return render(request, 'settings.html')

@login_required
def profile_settings(request):
    """Profile settings view"""
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # Update user profile
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                # You can add file handling logic here
                pass
            
            try:
                user.save()
                # Update member profile if exists
                if hasattr(user, 'member'):
                    member = user.member
                    member.phone_number = request.POST.get('phone', '')
                    member.save()
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        
        elif 'change_password' in request.POST:
            # Change password
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed successfully!')
                    # Re-authenticate user
                    from django.contrib.auth import update_session_auth_hash
                    update_session_auth_hash(request, user)
                else:
                    messages.error(request, 'New passwords do not match!')
            else:
                messages.error(request, 'Current password is incorrect!')
        
        elif 'update_notifications' in request.POST:
            # Update notification preferences
            # You can store these in user profile or separate model
            messages.success(request, 'Notification preferences updated!')
        
        elif 'delete_account' in request.POST:
            # Handle account deletion (be very careful with this)
            messages.warning(request, 'Account deletion feature is disabled for safety.')
        
        return redirect('profile_settings')
    
    return render(request, 'profile_settings.html')
