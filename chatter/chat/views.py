from django.shortcuts import render,get_object_or_404,redirect,reverse
from . import models
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import ChatRoomForm,PrivateChatRoomForm
from django.http import Http404
from django.contrib.auth import get_user_model


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

class PrivateRoomCreate(View):
    '''Class to create a view to create a private chat room between 2 users'''

    model = models.PrivateChatRoom
    template = 'chat/private_room_create.html'
    form = PrivateChatRoomForm

    def get(self,request):
        print(True)
        return render(request,self.template,context={'form':self.form()})

    def post(self, request):
        user_model = get_user_model()
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data['username']
            user2 = user_model.objects.get(username=username)
            if not self.model.objects.filter(user1=request.user, user2=user2).exists() and  not self.model.objects.filter(user1=user2, user2=request.user).exists():
                new_private_room = self.model.objects.create(user1=request.user, user2=user2)
                print(new_private_room)
                new_private_room.save()
                new_private_room.join(request.user)
                new_private_room.join(user2)
                return reverse('private_chat_room',kwargs={'pk':new_private_room.pk})
            else:
                if self.model.objects.filter(user1=request.user, user2=user2).exists():
                    private_room = self.model.objects.get(user1=request.user, user2=user2)

                    return redirect(private_room)
                if self.model.objects.filter(user1=user2, user2=request.user).exists():
                    private_room = self.model.objects.get(user1=user2,user2=request.user)
                    return redirect(private_room)

        else:
            return render(request,self.template,context={'form':bound_form})




class PrivateRoomView(View):
    '''Class to create a view to display/create a private room between 2 users'''

    template = 'chat/privatechat.html'
    model = models.PrivateChatRoom

    def get(self,request,pk):
        user = request.user
        room = get_object_or_404(self.model,pk=pk)
        messages = models.PrivateMessage.objects.filter(private_room = room.pk)
        if room.user1 == user or room.user2 == user:
            return render(request,self.template,context={'room':room,'messages':messages})
        else:
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




