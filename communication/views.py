from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    """Display user notifications"""
    return render(request, 'communication/notifications.html')

@login_required
def sms_alerts(request):
    """Display SMS alerts dashboard"""
    return render(request, 'communication/sms_alerts.html')

@login_required
def announcements(request):
    """Display announcements"""
    return render(request, 'communication/announcements.html')

@login_required
def send_announcement(request):
    """Send a new announcement"""
    return render(request, 'communication/send_announcement.html')
