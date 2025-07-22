from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def accident_list(request):
    return render(request, 'accidents/list.html')

@login_required
def report_accident(request):
    return render(request, 'accidents/report.html')

@login_required
def my_reports(request):
    """View user's own accident reports"""
    return render(request, 'accidents/my_reports.html')

@login_required
def analytics(request):
    """View accident analytics and statistics"""
    return render(request, 'accidents/analytics.html')

@login_required
def accident_detail(request, report_id):
    return render(request, 'accidents/detail.html')

@login_required
def update_accident(request, report_id):
    return render(request, 'accidents/update.html')

@login_required
def send_alerts(request, report_id):
    return render(request, 'accidents/alerts.html')

@login_required
def add_responders(request, request_id):
    return render(request, 'accidents/responders.html')
