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
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes
from .tokens import account_activation
from django.contrib import messages
from django.contrib.auth import get_user_model




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

class SingUpView(View):
    '''Class to create a view for signup process'''

    form_class = SignUpForm
    template_name = 'user/signup.html'

    def get(self,request):
        return render(request,self.template_name,context={'form':self.form_class()})

    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.update_or_create(user=user, defaults={'username':user.get_username()})
            site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string('user/account_activation_email.html',
                                       {
                                           'user':user,
                                           'domain':site.domain,
                                           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':account_activation.make_token(user)
                                       })
            user.email_user(subject,message)
            messages.success(request,'Please check your email')
            return redirect('dj-auth:login')
        else:
            return render(request,self.template_name,context={'form':bound_form})


class AccountActivationView(View):
    '''Class to construct a view to activate user account'''


    def get(self,request,uidb64,token,*args,**kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user_model = get_user_model()
            user= user_model.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError):
            user =None

        if user != None and account_activation.check_token(user,token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            Profile.objects.update_or_create(user=user,defaults={''})
            return redirect('dj-auth:login')
        else:
            messages.warning(request,'Confirmation link is no longer valid')
            return redirect('dj-auth:signup')




