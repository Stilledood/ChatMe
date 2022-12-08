from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import ChatRoomForm


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


class CreateRoomView(View):
    '''Class to create a view to allow user to create rooms'''

    model = models.ChatRoom
    template = 'chat/create_room.html'
    form_class = ChatRoomForm

    def get(self,request):
        return render(request,self.template,context={'form':self.form_class()})

    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_room = bound_form.save()
            return redirect(new_room)
        else:
            return render(request,self.template,context={'form':bound_form})


class DeleteRoomView(View):
    template = 'chat/delete_room.html'
    model = models.ChatRoom

    def get(self,request,room_name):
        room = get_object_or_404(self.model, name=room_name)
        return render(request,self.template,context={'room':room})

    def post(self,request,room_name):
        room = get_object_or_404(self.model, name=room_name)
        room.delete()
        return redirect('messenger')





class CategoriesList(View):
    '''Class to create a view to display all room categories from database'''

    model = models.RoomCategory
    template = 'chat/categories.html'

    def get(self,request):
        categories = self.model.objects.all()
        return render(request,self.template,context={'categories':categories})

class CategoryDetailsView(View):
    '''Class to create a view to display all the rooms from a selected category'''

    model = models.RoomCategory
    template = 'char/category_details.html'

    def get(self,request,name):

        category = get_object_or_404(self.model, name=name)
        rooms = category.chatroom_set.all()
        context = {
            'category' : category,
            'rooms' : rooms
        }
        return render(request,self.template,context=context)




