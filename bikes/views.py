from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def bike_list(request):
    return render(request, 'bikes/list.html')

@login_required
def register_bike(request):
    return render(request, 'bikes/register.html')

@login_required
def my_bikes(request):
    return render(request, 'bikes/my_bikes.html')

@login_required
def bike_detail(request, bike_id):
    return render(request, 'bikes/detail.html')

@login_required
def edit_bike(request, bike_id):
    return render(request, 'bikes/edit.html')

@login_required
def transfer_bike(request, bike_id):
    return render(request, 'bikes/transfer.html')

@login_required
def ownership_records(request):
    return render(request, 'bikes/ownership_records.html')

@login_required
def bike_documents(request, bike_id):
    return render(request, 'bikes/documents.html')

@login_required
def upload_document(request, bike_id):
    return render(request, 'bikes/upload_document.html')

@login_required
def lost_bike_tracking(request):
    """Lost bike tracking and inter-organization communication"""
    from stages.models import InterOrgCommunication
    lost_bikes = InterOrgCommunication.objects.filter(
        communication_type='lost_bike'
    ).order_by('-created_at')
    context = {'lost_bikes': lost_bikes}
    return render(request, 'bikes/lost_tracking.html', context)
