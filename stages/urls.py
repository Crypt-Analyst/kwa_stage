from django.urls import path
from . import views

app_name = 'stages'

urlpatterns = [
    path('', views.stage_list, name='list'),
    path('my-stage/', views.my_stage, name='my_stage'),
    path('detail/<int:stage_id>/', views.stage_detail, name='detail'),
    path('management/', views.stage_management, name='management'),
    path('add-member/<int:stage_id>/', views.add_member, name='add_member'),
    path('remove-member/<int:stage_id>/<int:member_id>/', views.remove_member, name='remove_member'),
    path('leadership/<int:stage_id>/', views.manage_leadership, name='leadership'),
    path('create/', views.create_stage, name='create'),
    path('map-view/', views.map_view, name='map_view'),
    path('reports/', views.stage_reports, name='reports'),
    path('api/save-coordinates/', views.save_stage_coordinates, name='save_coordinates'),
]
