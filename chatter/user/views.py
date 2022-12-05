from django.shortcuts import render
from .forms import SignUpForm, ProfileForm
from .models import Profile
from django.contrib.auth import get_user, logout
from django.conf import settings
from django.views import View



class UserProfile(View):
    '''Class to construct a view to display a user profile'''

    model= Profile
    template = 'user/profile.html'

    def get(self,request,username):
        profile =  self.model.objects.get(username = username)
        return render(request,self.template,context={'user':profile})


