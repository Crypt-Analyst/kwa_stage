from django.urls import path
from . import views

app_name = 'accidents'

urlpatterns = [
    path('', views.accident_list, name='list'),
    path('report/', views.report_accident, name='report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('analytics/', views.analytics, name='analytics'),
    path('detail/<int:report_id>/', views.accident_detail, name='detail'),
    path('update/<int:report_id>/', views.update_accident, name='update'),
    path('alerts/<int:report_id>/', views.send_alerts, name='send_alerts'),
    path('responders/<int:report_id>/', views.add_responders, name='add_responders'),
]
