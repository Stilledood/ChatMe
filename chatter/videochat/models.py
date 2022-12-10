from django.db import models
from django.conf import settings
import uuid


class PrivateVideoChatRoom(models.Model):
    '''Class to create a model for a private video chat room between 2 users'''

    videouser1 = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='videouser1')
    videouser2 = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='videouser2')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return f"VideoChat between : {self.videouser1.username} and {self.videouser2.username}"

