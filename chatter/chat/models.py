from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from autoslug import AutoSlugField
from django.shortcuts import reverse
import uuid


class RoomCategory(models.Model):
    '''Class to create a model for room category'''

    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to='category_images',default='stream-08.jpg')

    def __str__(self):
        return f"Category:{self.slug}"

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})







class ChatRoom(models.Model):
    '''Class to construct a model class for general chat rooms'''

    name = models.CharField(max_length=128,unique=True)
    online = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='members')
    room_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    admin_created_room = models.BooleanField(default=False)
    room_image = models.ImageField(upload_to='room_images', default='clip-02.jpg')
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-date_created','name']
        get_latest_by ='date_created'

    def __str__(self):
        return f"Room: {self.name}"

    def get_absolute_url(self):
        return reverse('room_details', kwargs={'room_name':self.name})

    def get_update_url(self):
        return reverse('user_chatroom_update', kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('user_chatroom_delete', kwargs={'pk':self.pk})

    def get_online_count(self):
        return self.online.count()

    def join(self,user):
        self.online.add(user)
        self.save()

    def leave(self,user):
        self.online.remove(user)
        self.save()


class PrivateChatRoom(models.Model):
    '''Class to create a model for private chat rooms'''

    online = models.ManyToManyField(User,blank=True)
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1')
    user2= models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    room_image = models.ImageField(upload_to='private_room_images', default='popular-8.jpg')

    def __str__(self):
        return f"Direct chat between:{self.user1.username} and {self.user2.username}"

    def get_online_count(self):
        return self.online.count()

    def get_absolute_url(self):
        return reverse('private_chat_room', kwargs={'pk':self.id})

    def join(self,user):
        self.online.add(user)
        self.save()

    def leave(self,user):
        self.online.remove(user)
        self.save()

class Message(models.Model):
    '''Class to construct a model for messages from multiuser rooms'''

    user= models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Public Message:{self.user.username}:{self.content} [{self.timestamp}]"


class PrivateMessage(models.Model):
    '''Class to construct a model for messages from private chat rooms'''

    private_sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='private_sender')
    private_receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='private_receiver')
    private_room = models.ForeignKey(PrivateChatRoom,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Private Message from :{self.private_sender.username} to {self.private_receiver.username}: {self.content} [{self.timestamp}]"





