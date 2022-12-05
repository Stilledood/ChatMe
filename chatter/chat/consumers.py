import json
from .models import ChatRoom,Message
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
            self.room_group_name,{"type":"chat_message", "message":message, 'user':self.user.username}
        )
        self.send(text_data=json.dumps({'message':message,'type':'chat_message', 'user':self.user.username}))

        Message.objects.create(user = self.user,room =self.room, content = message)


    # Receive messages from room group
    def chat_message(self,event):
        message = event['message']
        user = event["user"]

        #Send message to websocket
        self.send(text_data=json.dumps({ "message":message,'user':user}))