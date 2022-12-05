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

    def __str__(self):
        return f"Category:{self.slug}"

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})







class ChatRoom(models.Model):
    '''Class to construct a model class for general chat rooms'''

    name = models.CharField(max_length=128)
    online = models.ManyToManyField(User,blank=True,related_name='members')
    room_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    admin_created_room = models.BooleanField(default=False)

    def __str__(self):
        return f"Room: {self.name}"

    def get_absolute_url(self):
        return reverse('user_chatroom_details', kwargs={'pk':self.pk})

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


class PrivateCharRoom(models.Model):
    '''Class to create a model for private chat rooms'''

    online = models.ManyToManyField(User,blank=True)
    user1 = models.ForeignKey(User,on_delete=models.CASCADE)
    user2= models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)

    def __str__(self):
        return f"Direct chat between:{self.user1.username} and {self.user2.username}"

    def get_online_count(self):
        return self.online.count()

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
    


