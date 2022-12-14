from django.urls import path,re_path

from . import views


urlpatterns = [
    path("messenger/", views.DefaultChatRoomList.as_view(), name ='messenger'),
    path('messenger/categories/', views.CategoriesList.as_view(), name ='categories'),
    path('messenger/all_rooms/', views.AllRoomsView.as_view(), name='all_rooms'),
    path("messenger/chat_room/<str:room_name>/", views.ConnectToRoom.as_view(), name='room'),
    path('messenger/chat_room/<str:room_name>/details/', views.RoomDetailsView.as_view(), name='room_details'),
    path('messenger/chat_room/<str:room_name>/disconnect/',views.RoomDisconnect.as_view(), name='disconnect'),
    path('messenger/chat_room/<str:room_name>/delete/', views.DeleteRoomView.as_view(), name='delete_room'),
    path('messenger/chat_room/create/', views.CreateRoomView.as_view(), name= 'create_room'),
    path('messenger/private_room/create/', views.PrivateRoomCreate.as_view(), name='create_private_chat'),
    path('messenger/private_room/<str:pk>/',views.PrivateRoomView.as_view(), name='private_chat_room'),
    path('messenger/categories/', views.CategoriesList.as_view(), name='categories'),
    path('messenger/categories/<str:name>/', views.CategoryDetailsView.as_view(), name='category_details'),

]