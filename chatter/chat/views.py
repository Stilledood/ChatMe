from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View


class DefaultChatRoomList(View):
    '''Class to create a view to display all available chat rooms'''

    model = models.ChatRoom
    template = 'chat/index.html'

    def get(self,request):
        room_list = self.model.objects.filter(admin_created_room=True)
        return render(request,self.template, context={'rooms':room_list})


class ConnectToRoom(View):
    model = models.ChatRoom
    template = 'chat/room.html'

    def get(self,request,room_name):
        room = get_object_or_404(self.model, name=room_name)
        users = room.online.all()
        current_user = request.user
        if current_user not in room.online.all():
            room.join(current_user)
        return render(request, template_name=self.template, context={'room_name':room,'users':users})

class RoomDisconnect(View):
    model = models.ChatRoom

    def get(self,request,room_name):
        room = get_object_or_404(self.model,name=room_name)
        user = request.user
        room.leave(user)
        return redirect('messenger')

