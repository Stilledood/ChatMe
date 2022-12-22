from django.urls import path
from . import views

urlpatterns = [
    path('', views.videochatlobbyviews, name='lobby'),
    path('room/', views.videochatroomviews, name='room'),
    path('get_token/', views.getToken),
    path('create_member/', views.createMember),
    path('room/get_member/', views.getMember),
    path('delete_member/', views.deleteMember)
]