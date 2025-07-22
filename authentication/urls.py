from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('2fa/verify/', views.two_factor_verify, name='two_factor_verify'),
    path('2fa/setup/', views.two_factor_setup, name='two_factor_setup'),
    path('2fa/backup-tokens/', views.backup_tokens, name='backup_tokens'),
    path('security/', views.security_settings, name='security_settings'),
    path('send-verification/', views.send_verification_email, name='send_verification'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('generate-qr/', views.generate_qr_code, name='generate_qr'),
    path('google-signin/', views.google_signin, name='google_signin'),
]
