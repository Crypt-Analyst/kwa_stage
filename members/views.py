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
    except Member.DoesNotExist:
        return redirect('members:profile_setup')
    context = {'member': member}
    return render(request, 'members/profile.html', context)

def create_new_stage(stage_name):
    """Create a new stage with user-provided name"""
    from datetime import datetime
    from stages.models import Organization
    
    # Get default organization or create one
    organization = Organization.objects.first()
    if not organization:
        # Create default organization if none exists
        admin_user = User.objects.first()
        organization = Organization.objects.create(
            name="KwaStage Boda Boda Welfare",
            organization_type='welfare_society',
            registration_number='KWS-001-2025',
            description='Main boda boda welfare organization',
            phone_number='+254700000000',
            email='info@kwastage.ke',
            county='nairobi',
            sub_county='Nairobi Central',
            town='nairobi',
            address='Nairobi, Kenya',
            admin_user=admin_user
        )
    
    # Create the new stage
    stage = Stage.objects.create(
        name=stage_name,
        organization=organization,
        location=f"{stage_name} Area",
        county='Not Specified',
        sub_county='Not Specified',
        ward='Not Specified',
        registration_date=datetime.now().date(),
        description=f'User-created stage: {stage_name}',
        is_active=True
    )
    
    return stage

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
            'stage_name': existing_member.stage.name if existing_member.stage else '',
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
                'date_of_birth', 'address', 'zone', 
                'next_of_kin_name', 'next_of_kin_relationship', 
                'next_of_kin_phone', 'next_of_kin_id'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not request.POST.get(field, '').strip():
                    missing_fields.append(field.replace('_', ' ').title())
            
            # Check stage requirement (this is handled separately now in the stage processing section)
            # Stage validation moved to the stage processing section below
            
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
            
            # Get stage (existing or create new)
            stage_id = request.POST.get('stage_id', '').strip()
            stage_name = request.POST.get('stage_name', '').strip()
            
            if not stage_name:
                missing_fields.append('Stage Name')
            else:
                if stage_id and stage_id != 'new' and stage_id.isdigit():
                    # Existing stage selected
                    try:
                        stage = Stage.objects.get(id=stage_id)
                    except Stage.DoesNotExist:
                        # Fall back to creating new stage if ID doesn't exist
                        stage = create_new_stage(stage_name)
                        messages.success(request, f'New stage "{stage_name}" has been created and will be available for other users.')
                else:
                    # New stage - check if it already exists by name
                    existing_stage = Stage.objects.filter(name__iexact=stage_name).first()
                    if existing_stage:
                        stage = existing_stage
                        messages.info(request, f'Found existing stage: "{stage.name}"')
                    else:
                        # Create completely new stage
                        stage = create_new_stage(stage_name)
                        messages.success(request, f'New stage "{stage_name}" has been created and will be available for other users.')
            
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
    except Member.DoesNotExist:
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
