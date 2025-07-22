from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Member, MemberDocument
from stages.models import Stage

@login_required
def member_list(request):
    """List all members"""
    members = Member.objects.filter(status='active').select_related('user', 'stage')
    context = {'members': members}
    return render(request, 'members/list.html', context)

@login_required
def member_register(request):
    """Register new member"""
    if request.method == 'POST':
        # Handle member registration
        pass
    stages = Stage.objects.filter(is_active=True)
    context = {'stages': stages}
    return render(request, 'members/register.html', context)

@login_required
def member_profile(request):
    """View/edit member profile"""
    try:
        member = request.user.member
    except:
        return redirect('members:profile_setup')
    context = {'member': member}
    return render(request, 'members/profile.html', context)

@login_required
def profile_setup(request):
    """Setup member profile for new users or update existing profile"""
    form_data = {}
    
    # Check if member already exists
    existing_member = None
    try:
        existing_member = request.user.member
        # Pre-populate form with existing data
        form_data = {
            'first_name': existing_member.user.first_name,
            'last_name': existing_member.user.last_name,
            'national_id': existing_member.national_id,
            'phone_number': existing_member.phone_number,
            'date_of_birth': existing_member.date_of_birth.strftime('%Y-%m-%d') if existing_member.date_of_birth else '',
            'address': existing_member.address,
            'stage': existing_member.stage.id if existing_member.stage else '',
            'zone': existing_member.zone,
            'sacco': existing_member.sacco,
            'next_of_kin_name': existing_member.next_of_kin_name,
            'next_of_kin_relationship': existing_member.next_of_kin_relationship,
            'next_of_kin_phone': existing_member.next_of_kin_phone,
            'next_of_kin_id': existing_member.next_of_kin_id,
            'dependents_count': existing_member.dependents_count,
        }
    except Member.DoesNotExist:
        pass
    
    if request.method == 'POST':
        # Preserve form data
        form_data.update(request.POST.dict())
        
        try:
            # Validate required fields
            required_fields = [
                'first_name', 'last_name', 'national_id', 'phone_number', 
                'date_of_birth', 'address', 'stage', 'zone', 
                'next_of_kin_name', 'next_of_kin_relationship', 
                'next_of_kin_phone', 'next_of_kin_id'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not request.POST.get(field, '').strip():
                    missing_fields.append(field.replace('_', ' ').title())
            
            if missing_fields:
                messages.error(request, f'Please fill in all required fields: {", ".join(missing_fields)}')
                raise ValueError("Missing required fields")
            
            # Validate phone number format
            phone_number = request.POST.get('phone_number', '').strip()
            if not phone_number.startswith('+254') and not phone_number.startswith('254'):
                if phone_number.startswith('0'):
                    phone_number = '+254' + phone_number[1:]
                else:
                    phone_number = '+254' + phone_number
            elif phone_number.startswith('254'):
                phone_number = '+' + phone_number
            
            # Validate National ID
            national_id = request.POST.get('national_id', '').strip()
            if not national_id.isdigit() or len(national_id) != 8:
                messages.error(request, 'National ID must be exactly 8 digits.')
                raise ValueError("Invalid National ID")
            
            # Check if National ID already exists (only for new members or when changing ID)
            if not existing_member or existing_member.national_id != national_id:
                if Member.objects.filter(national_id=national_id).exists():
                    messages.error(request, 'A member with this National ID already exists.')
                    raise ValueError("Duplicate National ID")
            
            # Update user information
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.save()
            
            # Get stage
            stage_id = request.POST.get('stage')
            stage = get_object_or_404(Stage, id=stage_id)
            
            if existing_member:
                # Update existing member
                member = existing_member
                member.national_id = national_id
                member.phone_number = phone_number
                member.stage = stage
                member.zone = request.POST.get('zone', '').strip()
                member.sacco = request.POST.get('sacco', '').strip()
                member.next_of_kin_name = request.POST.get('next_of_kin_name', '').strip()
                member.next_of_kin_relationship = request.POST.get('next_of_kin_relationship')
                member.next_of_kin_phone = request.POST.get('next_of_kin_phone', '').strip()
                member.next_of_kin_id = request.POST.get('next_of_kin_id', '').strip()
                member.date_of_birth = request.POST.get('date_of_birth')
                member.address = request.POST.get('address', '').strip()
                member.dependents_count = int(request.POST.get('dependents_count', 0))
                
                # Handle profile photo
                if 'profile_photo' in request.FILES:
                    profile_photo = request.FILES['profile_photo']
                    # Validate file size (max 5MB)
                    if profile_photo.size > 5 * 1024 * 1024:
                        messages.error(request, 'Profile photo must be less than 5MB.')
                        raise ValueError("File too large")
                    
                    member.profile_photo = profile_photo
                
                member.save()
                messages.success(request, 'Profile updated successfully!')
                
            else:
                # Generate member number for new member
                import random
                member_number = f"KWS{random.randint(1000, 9999)}"
                while Member.objects.filter(member_number=member_number).exists():
                    member_number = f"KWS{random.randint(1000, 9999)}"
                
                # Create new member profile
                member = Member.objects.create(
                    user=request.user,
                    national_id=national_id,
                    phone_number=phone_number,
                    stage=stage,
                    zone=request.POST.get('zone', '').strip(),
                    sacco=request.POST.get('sacco', '').strip(),
                    next_of_kin_name=request.POST.get('next_of_kin_name', '').strip(),
                    next_of_kin_relationship=request.POST.get('next_of_kin_relationship'),
                    next_of_kin_phone=request.POST.get('next_of_kin_phone', '').strip(),
                    next_of_kin_id=request.POST.get('next_of_kin_id', '').strip(),
                    date_of_birth=request.POST.get('date_of_birth'),
                    address=request.POST.get('address', '').strip(),
                    member_number=member_number,
                    dependents_count=int(request.POST.get('dependents_count', 0))
                )
                
                # Handle profile photo
                if 'profile_photo' in request.FILES:
                    profile_photo = request.FILES['profile_photo']
                    # Validate file size (max 5MB)
                    if profile_photo.size > 5 * 1024 * 1024:
                        messages.error(request, 'Profile photo must be less than 5MB.')
                        raise ValueError("File too large")
                    
                    member.profile_photo = profile_photo
                    member.save()
                
                messages.success(request, 'Profile completed successfully! Welcome to KwaStage family.')
            
            return redirect('dashboard')
            
        except ValueError as ve:
            # Keep form data for re-display
            pass
        except Exception as e:
            messages.error(request, f'Error completing profile: {str(e)}')
    
    stages = Stage.objects.filter(is_active=True)
    context = {
        'stages': stages,
        'form_data': form_data,
        'existing_member': existing_member
    }
    return render(request, 'members/profile_setup.html', context)

@login_required
def edit_member(request, member_id):
    """Edit member details"""
    member = get_object_or_404(Member, id=member_id)
    context = {'member': member}
    return render(request, 'members/edit.html', context)

@login_required
def member_detail(request, member_id):
    """View member details"""
    member = get_object_or_404(Member, id=member_id)
    context = {'member': member}
    return render(request, 'members/detail.html', context)

@login_required
def member_documents(request):
    """View member documents"""
    try:
        member = request.user.member
        documents = member.documents.all()
    except:
        documents = []
    context = {'documents': documents}
    return render(request, 'members/documents.html', context)

@login_required
def member_search(request):
    """Search members"""
    query = request.GET.get('q', '')
    members = []
    if query:
        members = Member.objects.filter(
            user__first_name__icontains=query
        ).select_related('user', 'stage')
    context = {'members': members, 'query': query}
    return render(request, 'members/search.html', context)

@login_required
def add_member(request):
    """Add new member view"""
    if request.method == 'POST':
        # Handle member addition
        pass
    return render(request, 'members/add.html')

@login_required
def leadership(request):
    """Leadership view"""
    from stages.models import StageLeadership
    leaders = StageLeadership.objects.filter(is_current=True).select_related('member', 'stage')
    context = {'leaders': leaders}
    return render(request, 'members/leadership.html', context)
