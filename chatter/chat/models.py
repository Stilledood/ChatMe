from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from autoslug import AutoSlugField
from django.shortcuts import reverse


class RoomCategory(models.Model):
    '''Class to create a model for room category'''

    name = models.CharField(max_length=64, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return f"Category:{self.slug}"

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})







class UserChatRoom(models.Model):
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





