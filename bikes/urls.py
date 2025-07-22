from django.urls import path
from . import views

app_name = 'bikes'

urlpatterns = [
    path('', views.bike_list, name='list'),
    path('register/', views.register_bike, name='register'),
    path('my-bikes/', views.my_bikes, name='my_bikes'),
    path('detail/<int:bike_id>/', views.bike_detail, name='detail'),
    path('edit/<int:bike_id>/', views.edit_bike, name='edit'),
    path('transfer/<int:bike_id>/', views.transfer_bike, name='transfer'),
    path('ownership-records/', views.ownership_records, name='ownership_records'),
    path('documents/<int:bike_id>/', views.bike_documents, name='documents'),
    path('upload-document/<int:bike_id>/', views.upload_document, name='upload_document'),
    path('lost-tracking/', views.lost_bike_tracking, name='lost_tracking'),
]
