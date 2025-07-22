from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import Stage
import json

@login_required
def stage_list(request):
    stages = Stage.objects.all().order_by('-created_at')
    context = {
        'stages': stages
    }
    return render(request, 'stages/list.html', context)

@login_required
def my_stage(request):
    return render(request, 'stages/my_stage.html')

@login_required
def stage_detail(request, stage_id):
    try:
        stage = Stage.objects.get(id=stage_id)
        context = {
            'stage': stage
        }
        return render(request, 'stages/detail.html', context)
    except Stage.DoesNotExist:
        messages.error(request, 'Stage not found.')
        return redirect('stages:list')

@login_required
def stage_management(request):
    return render(request, 'stages/management.html')

@login_required
def add_member(request, stage_id):
    return render(request, 'stages/add_member.html')

@login_required
def remove_member(request, stage_id, member_id):
    return render(request, 'stages/remove_member.html')

@login_required
def manage_leadership(request, stage_id):
    return render(request, 'stages/leadership.html')

@login_required
def create_stage(request):
    if request.method == 'POST':
        # Check if it's a manual form submission (has stage_name) or map submission (has coordinates)
        if 'stage_name' in request.POST:
            # Handle manual form submission
            stage_name = request.POST.get('stage_name')
            location = request.POST.get('location')
            description = request.POST.get('description', '')
            county = request.POST.get('county', '')
            sub_county = request.POST.get('sub_county', '')
            ward = request.POST.get('ward', '')
            phone_number = request.POST.get('phone_number', '')
            email = request.POST.get('email', '')
            registration_date = request.POST.get('registration_date')
            
            if stage_name and location:
                try:
                    stage = Stage.objects.create(
                        name=stage_name,
                        location=location,
                        description=description,
                        county=county,
                        sub_county=sub_county,
                        ward=ward,
                        phone_number=phone_number,
                        email=email,
                        registration_date=registration_date if registration_date else timezone.now().date(),
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    messages.success(request, f'Stage "{stage_name}" has been registered successfully!')
                    return redirect('stages:detail', stage_id=stage.id)
                except Exception as e:
                    messages.error(request, f'Error creating stage: {str(e)}')
            else:
                messages.error(request, 'Stage name and location are required.')
        
        else:
            # Handle stage creation with coordinates (from map)
            stage_name = request.POST.get('stage_name')
            description = request.POST.get('description')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            # Here you would save to database
            # For now, we'll just return success
            if stage_name and latitude and longitude:
                return JsonResponse({
                    'status': 'success',
                    'message': f'Stage "{stage_name}" created successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required fields'
                })
    
    return render(request, 'stages/create.html')

@login_required
def map_view(request):
    # Get existing stages from database
    stages = Stage.objects.all()
    existing_stages = []
    
    for stage in stages:
        stage_data = {
            'name': stage.name,
            'description': stage.description or 'No description available',
        }
        
        # Add coordinates if available
        if stage.latitude and stage.longitude:
            stage_data['latitude'] = float(stage.latitude)
            stage_data['longitude'] = float(stage.longitude)
        else:
            # Default coordinates (you can remove this or set to None)
            stage_data['latitude'] = -1.2921
            stage_data['longitude'] = 36.8219
            
        existing_stages.append(stage_data)
    
    # If no stages exist, add some sample data
    if not existing_stages:
        existing_stages = [
            {
                'name': 'Kencom Stage',
                'latitude': -1.2921,
                'longitude': 36.8219,
                'description': 'Main CBD stage'
            },
            {
                'name': 'Kawangware Stage', 
                'latitude': -1.2921,
                'longitude': 36.7219,
                'description': 'Dagoretti area stage'
            }
        ]
    
    context = {
        'existing_stages': existing_stages
    }
    return render(request, 'stages/map_view.html', context)

# Alias for create_stage
create = create_stage

@login_required
def stage_reports(request):
    return render(request, 'stages/reports.html')

@csrf_exempt
@login_required
def save_stage_coordinates(request):
    """API endpoint to save stage with coordinates"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stage_name = data.get('name')
            description = data.get('description', '')
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))
            
            # Save to Stage model
            stage = Stage.objects.create(
                name=stage_name,
                description=description,
                latitude=latitude,
                longitude=longitude,
                created_by=request.user
            )
            
            return JsonResponse({
                'status': 'success',
                'message': f'Stage "{stage_name}" registered successfully',
                'stage_id': stage.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
