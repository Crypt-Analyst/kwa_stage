from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def cases(request):
    return render(request, 'emergency/cases.html')

@login_required
def report_case(request):
    return render(request, 'emergency/report.html')

@login_required
def case_detail(request, case_id):
    return render(request, 'emergency/detail.html')

@login_required
def verify_case(request, case_id):
    return render(request, 'emergency/verify.html')

@login_required
def approve_case(request, case_id):
    return render(request, 'emergency/approve.html')

@login_required
def disburse_funds(request, case_id):
    return render(request, 'emergency/disburse.html')

@login_required
def family_support(request):
    return render(request, 'emergency/family_support.html')

@login_required
def add_support_record(request, case_id):
    return render(request, 'emergency/add_support.html')
