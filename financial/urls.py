"""
Financial Services URLs
"""
from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    # Dashboard
    path('', views.financial_dashboard, name='dashboard'),
    
    # SACCO Services
    path('sacco-providers/', views.sacco_providers, name='sacco_list'),
    path('saccos/<int:sacco_id>/', views.sacco_detail, name='sacco_detail'),
    path('saccos/<int:sacco_id>/apply/', views.apply_to_sacco, name='apply_to_sacco'),
    
    # Bank Services
    path('banks/', views.bank_providers, name='bank_providers'),
    path('banks/<int:bank_id>/', views.bank_detail, name='bank_detail'),
    path('banks/<int:bank_id>/apply/', views.apply_to_bank, name='apply_to_bank'),
    
    # Tools
    path('calculator/', views.loan_calculator, name='loan_calculator'),
    
    # User Applications
    path('my-applications/', views.my_applications, name='my_applications'),
    path('sacco-application/<uuid:app_id>/', views.sacco_application_detail, name='sacco_application_detail'),
    path('bank-application/<uuid:app_id>/', views.bank_application_detail, name='bank_application_detail'),
]
