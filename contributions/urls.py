from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('', views.contribution_list, name='list'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('my-history/', views.my_contributions, name='my_history'),
    path('welfare-account/', views.welfare_account, name='welfare_account'),
    path('plans/', views.contribution_plans, name='plans'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('reports/', views.financial_reports, name='reports'),
]
