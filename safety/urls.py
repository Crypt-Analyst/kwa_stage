from django.urls import path
from . import views

app_name = 'safety'

urlpatterns = [
    # Dashboard
    path('', views.safety_dashboard, name='dashboard'),
    
    # Insurance
    path('insurance/', views.insurance_list, name='insurance_list'),
    path('insurance/add/', views.add_insurance, name='add_insurance'),
    
    # Licenses & Permits
    path('licenses/', views.license_list, name='license_list'),
    path('licenses/add/', views.add_license, name='add_license'),
    
    # Safety Training
    path('training/', views.training_list, name='training_list'),
    path('training/add/', views.add_training, name='add_training'),
    
    # Safety Incidents
    path('incidents/', views.incident_list, name='incident_list'),
    path('incidents/report/', views.report_incident, name='report_incident'),
    
    # Compliance
    path('compliance/check/', views.compliance_check, name='compliance_check'),
]
