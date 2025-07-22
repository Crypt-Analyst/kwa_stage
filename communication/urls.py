from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('sms-alerts/', views.sms_alerts, name='sms_alerts'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/send/', views.send_announcement, name='send_announcement'),
]
