from django.urls import path
from . import views

urlpatterns = [
    path('', views.videochatlobbyviews, name='lobby'),
    path('videochatroom/', views.videochatroomviews, name='room'),
    path('get_token/', views.getToken),
    path('get_member/', views.getMember),
    path('delete_member/' views.deleteMember)
]