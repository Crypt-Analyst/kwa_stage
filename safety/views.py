from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import date, timedelta

from .models import Insurance, License, SafetyTraining, ComplianceChecklist, SafetyIncident
from .forms import InsuranceForm, LicenseForm, SafetyTrainingForm, SafetyIncidentForm


@login_required
def safety_dashboard(request):
    """
    Safety & Compliance dashboard
    """
    try:
        member = request.user.member
        
        # Get or create compliance checklist
        compliance, created = ComplianceChecklist.objects.get_or_create(member=member)
        if created:
            compliance.calculate_compliance_score()
        
        # Get recent items
        recent_insurances = Insurance.objects.filter(member=member)[:3]
        recent_licenses = License.objects.filter(member=member)[:3]
        recent_trainings = SafetyTraining.objects.filter(member=member)[:3]
        recent_incidents = SafetyIncident.objects.filter(
            Q(reporter=member) | Q(involved_member=member)
        )[:5]
        
        # Get expiring items
        expiring_soon_date = date.today() + timedelta(days=30)
        expiring_insurances = Insurance.objects.filter(
            member=member,
            end_date__lte=expiring_soon_date,
            status='active'
        )
        expiring_licenses = License.objects.filter(
            member=member,
            expiry_date__lte=expiring_soon_date,
            status='valid'
        )
        
        context = {
            'compliance': compliance,
            'recent_insurances': recent_insurances,
            'recent_licenses': recent_licenses,
            'recent_trainings': recent_trainings,
            'recent_incidents': recent_incidents,
            'expiring_insurances': expiring_insurances,
            'expiring_licenses': expiring_licenses,
        }
        
        return render(request, 'safety/dashboard.html', context)
    except:
        return redirect('members:profile_setup')


@login_required
def insurance_list(request):
    """
    List all insurance policies
    """
    member = request.user.member
    insurances = Insurance.objects.filter(member=member)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        insurances = insurances.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        insurances = insurances.filter(
            Q(policy_number__icontains=search_query) |
            Q(insurance_company__icontains=search_query) |
            Q(insurance_type__icontains=search_query)
        )
    
    paginator = Paginator(insurances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'safety/insurance_list.html', context)


@login_required
def add_insurance(request):
    """
    Add new insurance policy
    """
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.member = request.user.member
            insurance.save()
            messages.success(request, 'Insurance policy added successfully!')
            return redirect('safety:insurance_list')
    else:
        form = InsuranceForm()
    
    return render(request, 'safety/add_insurance.html', {'form': form})


@login_required
def license_list(request):
    """
    List all licenses and permits
    """
    member = request.user.member
    licenses = License.objects.filter(member=member)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        licenses = licenses.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        licenses = licenses.filter(
            Q(license_number__icontains=search_query) |
            Q(license_type__icontains=search_query) |
            Q(issuing_authority__icontains=search_query)
        )
    
    paginator = Paginator(licenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'safety/license_list.html', context)


@login_required
def add_license(request):
    """
    Add new license or permit
    """
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES)
        if form.is_valid():
            license_obj = form.save(commit=False)
            license_obj.member = request.user.member
            license_obj.save()
            messages.success(request, 'License/permit added successfully!')
            return redirect('safety:license_list')
    else:
        form = LicenseForm()
    
    return render(request, 'safety/add_license.html', {'form': form})


@login_required
def training_list(request):
    """
    List all safety training records
    """
    member = request.user.member
    trainings = SafetyTraining.objects.filter(member=member)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        trainings = trainings.filter(status=status_filter)
    
    # Filter by training type
    type_filter = request.GET.get('type')
    if type_filter:
        trainings = trainings.filter(training_type=type_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        trainings = trainings.filter(
            Q(training_title__icontains=search_query) |
            Q(trainer_name__icontains=search_query) |
            Q(training_institution__icontains=search_query)
        )
    
    paginator = Paginator(trainings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': search_query,
    }
    
    return render(request, 'safety/training_list.html', context)


@login_required
def add_training(request):
    """
    Add new safety training record
    """
    if request.method == 'POST':
        form = SafetyTrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.member = request.user.member
            training.save()
            messages.success(request, 'Training record added successfully!')
            return redirect('safety:training_list')
    else:
        form = SafetyTrainingForm()
    
    return render(request, 'safety/add_training.html', {'form': form})


@login_required
def incident_list(request):
    """
    List all safety incidents
    """
    member = request.user.member
    incidents = SafetyIncident.objects.filter(
        Q(reporter=member) | Q(involved_member=member)
    )
    
    # Filter by severity if provided
    severity_filter = request.GET.get('severity')
    if severity_filter:
        incidents = incidents.filter(severity=severity_filter)
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        incidents = incidents.filter(incident_type=type_filter)
    
    # Filter by resolution status
    resolved_filter = request.GET.get('resolved')
    if resolved_filter == 'true':
        incidents = incidents.filter(is_resolved=True)
    elif resolved_filter == 'false':
        incidents = incidents.filter(is_resolved=False)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        incidents = incidents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    paginator = Paginator(incidents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'severity_filter': severity_filter,
        'type_filter': type_filter,
        'resolved_filter': resolved_filter,
        'search_query': search_query,
    }
    
    return render(request, 'safety/incident_list.html', context)


@login_required
def report_incident(request):
    """
    Report a new safety incident
    """
    if request.method == 'POST':
        form = SafetyIncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user.member
            incident.save()
            messages.success(request, 'Safety incident reported successfully!')
            return redirect('safety:incident_list')
    else:
        form = SafetyIncidentForm()
    
    return render(request, 'safety/report_incident.html', {'form': form})


@login_required
def compliance_check(request):
    """
    Check and update compliance status
    """
    member = request.user.member
    compliance, created = ComplianceChecklist.objects.get_or_create(member=member)
    
    # Update compliance status based on current data
    compliance.bike_insurance_valid = Insurance.objects.filter(
        member=member,
        insurance_type__in=['bike_comprehensive', 'bike_third_party'],
        status='active',
        end_date__gt=date.today()
    ).exists()
    
    compliance.personal_insurance_valid = Insurance.objects.filter(
        member=member,
        insurance_type__in=['personal_accident', 'medical', 'life'],
        status='active',
        end_date__gt=date.today()
    ).exists()
    
    compliance.driving_license_valid = License.objects.filter(
        member=member,
        license_type='driving_license',
        status='valid',
        expiry_date__gt=date.today()
    ).exists()
    
    compliance.motorcycle_permit_valid = License.objects.filter(
        member=member,
        license_type='motorcycle_permit',
        status='valid',
        expiry_date__gt=date.today()
    ).exists()
    
    compliance.commercial_permit_valid = License.objects.filter(
        member=member,
        license_type='commercial_permit',
        status='valid',
        expiry_date__gt=date.today()
    ).exists()
    
    compliance.safety_training_completed = SafetyTraining.objects.filter(
        member=member,
        training_type__in=['defensive_driving', 'motorcycle_safety', 'road_safety'],
        status='completed',
        passed=True
    ).exists()
    
    compliance.first_aid_training_completed = SafetyTraining.objects.filter(
        member=member,
        training_type='first_aid',
        status='completed',
        passed=True
    ).exists()
    
    compliance.good_conduct_certificate = License.objects.filter(
        member=member,
        license_type='good_conduct',
        status='valid',
        expiry_date__gt=date.today()
    ).exists()
    
    # Calculate and save compliance score
    compliance.calculate_compliance_score()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'compliance_score': float(compliance.compliance_score),
            'message': f'Compliance updated. Current score: {compliance.compliance_score}%'
        })
    
    messages.success(request, f'Compliance updated. Current score: {compliance.compliance_score}%')
    return redirect('safety:dashboard')
