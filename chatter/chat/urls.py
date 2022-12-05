from django.urls import path

from . import views


urlpatterns = [
    path("messenger/", views.DefaultChatRoomList.as_view(), name ='index'),
    path("messenger/chat_room/<str:room_name>/",views.ConnectToRoom.as_view(), name='room'),
]