from django.urls import path

from . import views


urlpatterns = [
    path("messenger/", views.index, name ='index'),
    path("messenger/chat_room/<str:room_name>/",views.room, name='room'),
]