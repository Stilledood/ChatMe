import json
from .models import ChatRoom,Message,PrivateChatRoom,PrivateMessage
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User



class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args,kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']
        self.room = ChatRoom.objects.get(name=self.room_name)
        print(self.room)
        print(self.room.online.all())
        print(self.user.username)


        self.accept()
        #Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )


        self.send(text_data=json.dumps({
            'type':'user_list',
            'users':[user.username for user in self.room.online.all()]
        }))

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive messages from websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']




        #Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{ "type":"chat_message","message":message, 'user':self.user.username}
        )


        Message.objects.create(user = self.user,room =self.room, content = message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))


class DirectChatConsumer(WebsocketConsumer):
    '''Class to create a consumer for private chats between 2 users'''

    def __str__(self, *args, **kwargs):
        super().__init__(args,kwargs)
        self.user = None
        self.other_username = None
        self.other_user = None
        self.room = None
        self.room_group_name = None
        self.room_name = None

    #Called on connection
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name =f"chat_{self.room_name}"
        self.room = PrivateChatRoom.objects.get(pk=self.room_name)
        self.user = self.scope['user']

        if self.user == self.room.user1:
            self.other_user = User.objects.get(pk=self.room.user2.pk)
        else:
            self.other_user = User.objects.get(pk=self.room.user1.pk)

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.send(text_data=json.dumps({
            'type':'user_list',
            'users':[user.username for user in self.room.online.all()]
        }))


    def disconnect(self,close_code):
        self.room = PrivateChatRoom.objects.get(pk=self.room_name)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        saved_message = PrivateMessage.objects.create(private_sender=self.user, private_receiver = self.other_user,private_room=self.room,content=message)
        saved_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'user':self.user.username,

                'message':message
            },
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))