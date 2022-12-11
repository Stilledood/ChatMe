from .models import ChatRoom,PrivateChatRoom
from django.forms import ModelForm



class ChatRoomForm(ModelForm):
    '''Class to create a form for Group chat Room'''

    class Meta:
        model = ChatRoom
        fields = ['name', 'category', 'room_image']

class PrivateChatRoomForm(ModelForm):
    '''Class toi create a form to allow user to create private chat rooms'''

    class Meta:
        model = PrivateChatRoom
        fields = ['room_image']