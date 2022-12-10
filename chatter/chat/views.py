from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import ChatRoomForm
from django.http import Http404


# Public Room Views
class DefaultChatRoomList(View):
    '''Class to create a view to display all available chat rooms'''

    model = models.ChatRoom
    template = 'chat/index.html'

    def get(self,request):
        room_list = self.model.objects.filter(admin_created_room=True)
        return render(request,self.template, context={'rooms':room_list})


class RoomDetailsView(View):
    '''Class to create a view to display all the informations about a room'''

    model = models.ChatRoom
    template = 'chat/room_details.html'

    def get(self,request,room_name):
        room = get_object_or_404(self.model, name=room_name)
        return render(request,self.template,context={'room':room})


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


# Private Room Views

class PrivateRoomView(View):
    '''Class to create a view to display/create a private room between 2 users'''

    template_user1 = 'chat/userchat1.html'
    template_user2 = 'chat/userchat2.html'
    model = models.PrivateChatRoom

    def get(self,request,pk):
        current_user = request.user
        other_user = User.objects.get(pk=pk)

        if not self.model.objects.filter(user1==current_user, user2=other_user).exists() and not self.model.objects.filter(user1=other_user,user2=current_user).exists():
            room = self.model.objects.create(user1=current_user, user2=other_user)
            return render(request, self.template_name, context={'room':room})

        elif self.model.objects.filter(user1=current_user, user2=other_user).exists():
            room = self.model.get(user1=current_user, user2=other_user)
            chat_messages = []
            if current_user == room.user1:
                chat_messages = models.PrivateMessage.objects.filter(private_room=room)
                return render(request, self.template_user1,context={'room': room,
                                                                    'chat_messages': chat_messages})
        elif self.model.objects.filter(user1=other_user,user2=current_user).exists():
            room = self.model.get(user1=other_user, user2=current_user)
            chat_messages = []
            if current_user == room.user2:
                chat_messages = models.PrivateMessage.objects.filter(private_room=room)
                return render(request, self.template_user2, context={'room':room,
                                                                     'chat_messages':chat_messages})

        else:
            raise Http404('User not authorized for this chatroom')





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




