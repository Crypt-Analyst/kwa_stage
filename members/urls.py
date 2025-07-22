from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_list, name='list'),
    path('add/', views.add_member, name='add'),
    path('register/', views.member_register, name='register'),
    path('profile/', views.member_profile, name='profile'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('edit/<int:member_id>/', views.edit_member, name='edit'),
    path('detail/<int:member_id>/', views.member_detail, name='detail'),
    path('documents/', views.member_documents, name='documents'),
    path('search/', views.member_search, name='search'),
    path('leadership/', views.leadership, name='leadership'),
]
