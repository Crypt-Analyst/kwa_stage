from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.cases, name='cases'),
    path('report/', views.report_case, name='report_case'),
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    path('verify/<int:case_id>/', views.verify_case, name='verify_case'),
    path('approve/<int:case_id>/', views.approve_case, name='approve_case'),
    path('disburse/<int:case_id>/', views.disburse_funds, name='disburse_funds'),
    path('family-support/', views.family_support, name='family_support'),
    path('support-record/<int:case_id>/', views.add_support_record, name='add_support_record'),
]
