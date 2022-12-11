from .models import ChatRoom,PrivateChatRoom
from django.forms import ModelForm
from django import forms




class ChatRoomForm(ModelForm):
    '''Class to create a form for Group chat Room'''

    class Meta:
        model = ChatRoom
        fields = ['name', 'category', 'room_image']

class PrivateChatRoomForm(forms.Form):
    '''Class toi create a form to allow user to create private chat rooms'''

    username = forms.CharField(max_length=128)
