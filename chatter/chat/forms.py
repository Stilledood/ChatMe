from .models import ChatRoom
from django.forms import ModelForm



class ChatRoomForm(ModelForm):
    '''Class to create a form for Group chat Room'''

    class Meta:
        model = ChatRoom
        fields = ['name', 'category', 'room_image']

