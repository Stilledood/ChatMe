from django.shortcuts import render
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View


class DefaultChatRoomList(View):
    '''Class to create a view to display all available chat rooms'''

    model = models.ChatRoom
    template = 'chat/chatroom_list.html'

    def get(self,request):
        room_list = self.model.objects.filter(admin_created_room=True)
        return render(request,self.template, context={'rooms':room_list})


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    room, created = models.ChatRoom.objects.get_or_create(name=room_name)
    if room:
        room.join(User.objects.get(pk=request.user.id))
    elif created:
        created.join(User.pk)

    return render(request, "chat/room.html", {"room_name": room})