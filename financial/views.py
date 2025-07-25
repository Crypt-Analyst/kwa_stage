"""
Financial Services Views - SACCO and Bank Applications
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
import math

from .models import (
    SaccoProvider, BankProvider, SaccoApplication, 
    BankLoanApplication, ApplicationDocument, LoanCalculation
)
from members.models import Member

@login_required
def financial_dashboard(request):
    """Financial services dashboard"""
    try:
        member = request.user.member
        
        # Get user's applications
        sacco_applications = SaccoApplication.objects.filter(applicant=member).order_by('-created_at')[:5]
        bank_applications = BankLoanApplication.objects.filter(applicant=member).order_by('-created_at')[:5]
        
        # Combine recent applications
        recent_applications = []
        for app in sacco_applications:
            recent_applications.append(app)
        for app in bank_applications:
            recent_applications.append(app)
        
        # Sort by created date
        recent_applications.sort(key=lambda x: x.created_at, reverse=True)
        recent_applications = recent_applications[:5]
        
        # Get featured providers
        featured_saccos = SaccoProvider.objects.filter(
            is_active=True, 
            bodaboda_focused=True
        ).order_by('-created_at')[:3]
        
        featured_banks = BankProvider.objects.filter(
            is_active=True,
            offers_motorcycle_loans=True
        ).order_by('-created_at')[:3]
        
        # Statistics
        stats = {
            'total_saccos': SaccoProvider.objects.filter(is_active=True, bodaboda_focused=True).count(),
            'total_banks': BankProvider.objects.filter(is_active=True).count(),
            'user_applications': sacco_applications.count() + bank_applications.count(),
        }
        
        context = {
            'member': member,
            'stats': stats,
            'featured_saccos': featured_saccos,
            'featured_banks': featured_banks,
            'recent_applications': recent_applications,
            'sacco_applications': sacco_applications,
            'bank_applications': bank_applications,
        }
        
    except Member.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup first.')
        return redirect('members:profile_setup')
    
    return render(request, 'financial/dashboard.html', context)

@login_required
def sacco_providers(request):
    """List all SACCO providers"""
    # Search and filter
    search_query = request.GET.get('search', '')
    county_filter = request.GET.get('county', '')
    coverage_filter = request.GET.get('coverage', '')
    
    saccos = SaccoProvider.objects.filter(is_active=True, bodaboda_focused=True)
    
    if search_query:
        saccos = saccos.filter(
            Q(name__icontains=search_query) |
            Q(counties_served__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if county_filter:
        saccos = saccos.filter(counties_served__icontains=county_filter)
    
    if coverage_filter:
        saccos = saccos.filter(coverage_area__icontains=coverage_filter)
    
    # Pagination
    paginator = Paginator(saccos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all counties from counties_served field (comma-separated)
    all_counties_data = SaccoProvider.objects.filter(
        is_active=True, bodaboda_focused=True
    ).values_list('counties_served', flat=True)
    
    counties = set()
    for county_list in all_counties_data:
        if county_list:
            # Split comma-separated counties and clean them
            county_names = [county.strip() for county in county_list.split(',')]
            counties.update(county_names)
    
    counties = sorted(list(counties))
    
    # Coverage areas for filter
    coverage_areas = SaccoProvider.objects.filter(
        is_active=True, bodaboda_focused=True
    ).values_list('coverage_area', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'county_filter': county_filter,
        'coverage_filter': coverage_filter,
        'counties': counties,
        'coverage_areas': coverage_areas,
    }
    
    return render(request, 'financial/sacco_list.html', context)

@login_required
def sacco_detail(request, sacco_id):
    """SACCO provider detail page"""
    sacco = get_object_or_404(SaccoProvider, id=sacco_id, is_active=True)
    
    try:
        member = request.user.member
        # Check if user has pending applications
        existing_application = SaccoApplication.objects.filter(
            applicant=member, 
            sacco=sacco,
            status__in=['draft', 'submitted', 'under_review', 'pending_documents']
        ).first()
    except Member.DoesNotExist:
        member = None
        existing_application = None
    
    context = {
        'sacco': sacco,
        'existing_application': existing_application,
        'member': member,
    }
    
    return render(request, 'financial/sacco_apply.html', context)

@login_required
def apply_to_sacco(request, sacco_id):
    """Apply to a SACCO"""
    sacco = get_object_or_404(SaccoProvider, id=sacco_id, is_active=True)
    
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup first.')
        return redirect('members:profile_setup')
    
    # Check for existing pending applications
    existing_application = SaccoApplication.objects.filter(
        applicant=member, 
        sacco=sacco,
        status__in=['draft', 'submitted', 'under_review', 'pending_documents']
    ).first()
    
    if existing_application:
        messages.info(request, f'You already have a pending application with {sacco.name}.')
        return redirect('financial:sacco_application_detail', app_id=existing_application.application_id)
    
    if request.method == 'POST':
        # Create new application
        application = SaccoApplication.objects.create(
            applicant=member,
            sacco=sacco,
            application_type=request.POST.get('application_type'),
            requested_amount=request.POST.get('requested_amount', 0) or None,
            purpose=request.POST.get('purpose', ''),
            repayment_period_months=request.POST.get('repayment_period_months') or None,
            monthly_income=request.POST.get('monthly_income', 0),
            other_income_sources=request.POST.get('other_income_sources', ''),
            dependents_count=request.POST.get('dependents_count', 0),
            current_loans=request.POST.get('current_loans', ''),
            years_in_bodaboda=request.POST.get('years_in_bodaboda', 0),
            daily_earnings=request.POST.get('daily_earnings', 0),
            motorcycle_owned=request.POST.get('motorcycle_owned') == 'on',
            motorcycle_value=request.POST.get('motorcycle_value', 0) or None,
            route_description=request.POST.get('route_description', ''),
            stage_location=request.POST.get('stage_location', ''),
            guarantor1_name=request.POST.get('guarantor1_name', ''),
            guarantor1_phone=request.POST.get('guarantor1_phone', ''),
            guarantor1_id_number=request.POST.get('guarantor1_id_number', ''),
            guarantor1_relationship=request.POST.get('guarantor1_relationship', ''),
            guarantor2_name=request.POST.get('guarantor2_name', ''),
            guarantor2_phone=request.POST.get('guarantor2_phone', ''),
            guarantor2_id_number=request.POST.get('guarantor2_id_number', ''),
            guarantor2_relationship=request.POST.get('guarantor2_relationship', ''),
            status='draft'
        )
        
        messages.success(request, f'Application created successfully! Application ID: {application.application_id}')
        return redirect('financial:sacco_application_detail', app_id=application.application_id)
    
    context = {
        'sacco': sacco,
        'member': member,
    }
    
    return render(request, 'financial/sacco_apply.html', context)

@login_required
def bank_providers(request):
    """List all bank providers"""
    search_query = request.GET.get('search', '')
    
    banks = BankProvider.objects.filter(is_active=True, offers_motorcycle_loans=True)
    
    if search_query:
        banks = banks.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(banks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'financial/bank_list.html', context)

@login_required
def bank_detail(request, bank_id):
    """Bank provider detail page"""
    bank = get_object_or_404(BankProvider, id=bank_id, is_active=True)
    
    try:
        member = request.user.member
        # Check if user has pending applications
        existing_application = BankLoanApplication.objects.filter(
            applicant=member, 
            bank=bank,
            status__in=['draft', 'submitted', 'initial_review', 'credit_assessment', 'conditional_approval', 'documentation']
        ).first()
    except Member.DoesNotExist:
        member = None
        existing_application = None
    
    context = {
        'bank': bank,
        'existing_application': existing_application,
        'member': member,
    }
    
    return render(request, 'financial/bank_apply.html', context)

@login_required
def apply_to_bank(request, bank_id):
    """Redirect to bank's loan application page"""
    bank = get_object_or_404(BankProvider, id=bank_id, is_active=True)
    
    # Redirect directly to the bank's loan application page or website
    if hasattr(bank, 'loan_application_url') and bank.loan_application_url:
        return redirect(bank.loan_application_url)
    elif bank.website:
        return redirect(bank.website)
    else:
        # Show bank contact information if no direct link available
        context = {
            'bank': bank,
            'message': 'Please contact the bank directly to apply for a loan.',
        }
        return render(request, 'financial/bank_contact.html', context)
    
    context = {
        'bank': bank,
        'member': member,
    }
    
    return render(request, 'financial/bank_apply.html', context)

@login_required
def loan_calculator(request):
    """Loan calculator tool"""
    if request.method == 'POST':
        principal = Decimal(request.POST.get('principal', 0))
        rate = Decimal(request.POST.get('rate', 0)) / 100 / 12  # Monthly rate
        term = int(request.POST.get('term', 12))  # Months
        
        if principal > 0 and rate > 0 and term > 0:
            # Calculate monthly payment using PMT formula
            monthly_payment = principal * (rate * (1 + rate)**term) / ((1 + rate)**term - 1)
            total_amount = monthly_payment * term
            total_interest = total_amount - principal
            
            # Save calculation if user is logged in
            try:
                member = request.user.member
                LoanCalculation.objects.create(
                    member=member,
                    provider_type=request.POST.get('provider_type', 'sacco'),
                    provider_name=request.POST.get('provider_name', 'General'),
                    principal_amount=principal,
                    interest_rate=Decimal(request.POST.get('rate', 0)),
                    term_months=term,
                    monthly_payment=monthly_payment,
                    total_interest=total_interest,
                    total_amount=total_amount
                )
            except Member.DoesNotExist:
                pass
            
            return JsonResponse({
                'success': True,
                'monthly_payment': float(monthly_payment),
                'total_interest': float(total_interest),
                'total_amount': float(total_amount),
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid input values'})
    
    # Get recent calculations for the user
    recent_calculations = []
    try:
        member = request.user.member
        recent_calculations = LoanCalculation.objects.filter(member=member).order_by('-created_at')[:5]
    except Member.DoesNotExist:
        pass
    
    context = {
        'recent_calculations': recent_calculations,
    }
    
    return render(request, 'financial/loan_calculator.html', context)

@login_required
def my_applications(request):
    """User's applications dashboard"""
    try:
        member = request.user.member
        
        sacco_applications = SaccoApplication.objects.filter(applicant=member).order_by('-created_at')
        bank_applications = BankLoanApplication.objects.filter(applicant=member).order_by('-created_at')
        
        context = {
            'sacco_applications': sacco_applications,
            'bank_applications': bank_applications,
        }
        
    except Member.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup first.')
        return redirect('members:profile_setup')
    
    return render(request, 'financial/my_applications.html', context)

@login_required
def sacco_application_detail(request, app_id):
    """SACCO application detail"""
    try:
        member = request.user.member
        application = get_object_or_404(SaccoApplication, application_id=app_id, applicant=member)
    except Member.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup first.')
        return redirect('members:profile_setup')
    
    context = {
        'application': application,
    }
    
    return render(request, 'financial/application_detail.html', context)

@login_required
def bank_application_detail(request, app_id):
    """Bank application detail"""
    try:
        member = request.user.member
        application = get_object_or_404(BankLoanApplication, application_id=app_id, applicant=member)
    except Member.DoesNotExist:
        messages.warning(request, 'Please complete your profile setup first.')
        return redirect('members:profile_setup')
    
    context = {
        'application': application,
    }
    
    return render(request, 'financial/application_detail.html', context)
