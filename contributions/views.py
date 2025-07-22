from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def contribution_list(request):
    return render(request, 'contributions/list.html')

@login_required
def make_payment(request):
    return render(request, 'contributions/make_payment.html')

@login_required
def my_contributions(request):
    return render(request, 'contributions/my_history.html')

@login_required
def welfare_account(request):
    return render(request, 'contributions/welfare_account.html')

@login_required
def contribution_plans(request):
    return render(request, 'contributions/plans.html')

@login_required
def confirm_payment(request):
    return render(request, 'contributions/confirm.html')

def mpesa_callback(request):
    return JsonResponse({'status': 'received'})

@login_required
def financial_reports(request):
    """Financial reports view"""
    return render(request, 'contributions/reports.html')
