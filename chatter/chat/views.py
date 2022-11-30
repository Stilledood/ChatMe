from django.shortcuts import render
from . import models

def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    room, created = models.ChatRoom.objects.get_or_create(name=room_name)
    return render(request, "chat/room.html", {"room_name": room})