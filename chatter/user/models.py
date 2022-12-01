from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from PIL import Image
from django.shortcuts import reverse


class CustomUser(AbstractUser):
    '''Class to create a custom user class'''

    age = models.PositiveInteger(null =True, blank= True)
    friends = models.ManyToManyField('CustomUser', blank =True)


class Profile(models.Model):
    '''Class to construct a model for each CustomUser instance'''

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user', null=True)
    description = models.TextField(max_length=250, default='')


    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        return reverse('user_profile',kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('user_profile_update', kwargs={'slug':self.slug})

    def save(self,*args, **kwargs):
        super(Profile,self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save((self.image.path))


# Function to automatically create a profile when a user signup
@receiver(post_save, sender=CustomUser)
def create_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Function to save the profile after user signup
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()





