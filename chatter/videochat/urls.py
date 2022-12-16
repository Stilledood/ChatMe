from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name ='videochat_lobby'),
    path('pusher/auth/', views.pusher_auth, name= 'pusher_auth'),
    path('token/', views.generate_token , name = 'videochat-token')
]