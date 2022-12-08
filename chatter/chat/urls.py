from django.urls import path

from . import views


urlpatterns = [
    path("messenger/", views.DefaultChatRoomList.as_view(), name ='messenger'),
    path("messenger/chat_room/<str:room_name>/", views.ConnectToRoom.as_view(), name='room'),
    path('messenger/categories/', views.CategoriesList.as_view(), name='categories'),
    path('messenger/rooms/create/',views.CreateRoomView.as_view(), name='create_room'),
]