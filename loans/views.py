from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def loan_list(request):
    return render(request, 'loans/list.html')

@login_required
def apply_loan(request):
    return render(request, 'loans/apply.html')

@login_required
def my_loans(request):
    return render(request, 'loans/my_loans.html')

@login_required
def loan_detail(request, loan_id):
    return render(request, 'loans/detail.html')

@login_required
def approve_loan(request, loan_id):
    return render(request, 'loans/approve.html')

@login_required
def disburse_loan(request, loan_id):
    return render(request, 'loans/disburse.html')

@login_required
def make_repayment(request):
    return render(request, 'loans/repay.html')

@login_required
def loan_repayment(request, loan_id):
    return render(request, 'loans/repayment.html')

@login_required
def loan_kitty(request):
    return render(request, 'loans/kitty.html')

@login_required
def loan_calculator(request):
    return render(request, 'loans/calculator.html')

@login_required
def repayment_schedule(request):
    """Display repayment schedule for all loans"""
    return render(request, 'loans/repayment_schedule.html')

@login_required
def loan_reports(request):
    """Display loan reports and analytics"""
    return render(request, 'loans/reports.html')
