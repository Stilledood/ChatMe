from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm, ProfileForm
from .models import Profile
from django.contrib.auth import get_user, logout
from django.conf import settings
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse




class UserProfile(View):
    '''Class to construct a view to display a user profile'''

    model= Profile
    template = 'user/profile.html'

    def get(self,request,username):

        profile =  get_object_or_404(self.model,username=username)
        print(profile)
        return render(request,self.template,context={'profile':profile})


class DisableUserAccount(View):
    '''Class to create a view to allow a user to delete his/her account'''
    template_name = 'user/disable_account.html'

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self,request):
        return TemplateResponse(request,self.template_name)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self,request):
        user = request.user
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect('messenger')







