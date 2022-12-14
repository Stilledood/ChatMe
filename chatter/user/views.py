from django.shortcuts import render,redirect
from .forms import SignUpForm, ProfileForm
from .models import Profile
from django.contrib.auth import get_user, logout
from django.conf import settings
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator




class UserProfile(View):
    '''Class to construct a view to display a user profile'''

    model= Profile
    template = 'user/profile.html'

    def get(self,request,username):
        profile =  self.model.objects.get(username = username)
        return render(request,self.template,context={'user':profile})


class DisableUserAccount(View):
    '''Class to create a view to allow a user to delete his/her account'''
    template_name = 'user/disable_account.html'

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self,request):
        return render(request,self.template_name)

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def post(self,request):
        user = request.user
        user.set_unusable_password = True
        user.is_active = False
        user.save()
        logout(request)
        return redirect('messenger')







