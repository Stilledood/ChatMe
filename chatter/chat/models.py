from django.db import models


class ChatRoom(models.Model):
    '''Class to construct a model class for general chat rooms'''

    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Room: {self.name}"




