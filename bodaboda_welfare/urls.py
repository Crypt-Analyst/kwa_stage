"""
URL configuration for bodaboda_welfare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('auth/', include('authentication.urls')),
    path('login/', views.user_login, name='login'),  # Keep for backward compatibility
    path('logout/', views.user_logout, name='logout'),  # Keep for backward compatibility
    path('register/', views.register, name='register'),
    
    # Module URLs
    path('members/', include('members.urls', namespace='members')),
    path('contributions/', include('contributions.urls', namespace='contributions')),
    path('emergency/', include('emergency.urls', namespace='emergency')),
    path('accidents/', include('accidents.urls', namespace='accidents')),
    path('bikes/', include('bikes.urls', namespace='bikes')),
    path('stages/', include('stages.urls', namespace='stages')),
    path('loans/', include('loans.urls', namespace='loans')),
    path('communication/', include('communication.urls', namespace='communication')),
    path('social/', include('social.urls', namespace='social')),
    path('safety/', include('safety.urls', namespace='safety')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('financial/', include('financial.urls', namespace='financial')),
    
    # Module views from main app
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings, name='settings'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    
    # API URLs
    path('api/', include('rest_framework.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
