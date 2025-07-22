from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_list, name='list'),
    path('apply/', views.apply_loan, name='apply'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('detail/<int:loan_id>/', views.loan_detail, name='detail'),
    path('approve/<int:loan_id>/', views.approve_loan, name='approve'),
    path('disburse/<int:loan_id>/', views.disburse_loan, name='disburse'),
    path('repay/', views.make_repayment, name='repay'),
    path('repayment/<int:loan_id>/', views.loan_repayment, name='repayment'),
    path('repayment-schedule/', views.repayment_schedule, name='repayment_schedule'),
    path('reports/', views.loan_reports, name='reports'),
    path('kitty/', views.loan_kitty, name='kitty'),
    path('calculator/', views.loan_calculator, name='calculator'),
]
