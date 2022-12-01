from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from PIL import Image
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    '''Class to construct a profile model connected to each user instance'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defautl.jpg', upload_to='profile_pics')
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=128)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}'s Profile"

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username' : self.username})

    def get_update_url(self):
        return reverse('user_profile_details', kwargs={'username':self.username})

# Function to create a user profile when a user signup
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)






