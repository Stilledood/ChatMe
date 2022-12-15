from django.urls import re_path, path,include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .views import UserProfile,DisableUserAccount,SingUpView
from django.urls import reverse_lazy



app_name='user'

password_urlpatterns = [
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='user/change_password.html',success_url=reverse_lazy('dj-auth:password_change_done')),name='password_change'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html', extra_context ={'form':AuthenticationForm}),name='password_change_done'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name ='user/reset_password.html',success_url=reverse_lazy('dj-auth:password_reset_done'),email_template_name='user/password_reset_email.txt',subject_template_name='user/password_email_title.txt'), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    re_path(r'^reset_password/'
            r'(?P<uidb64>[0-9A-Za-z-\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',success_url=reverse_lazy('dj-auth:password_reset_complete')),name='password_reset_confirm'),
    path('reset_password/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html',extra_context={'form':AuthenticationForm}),name='password_reset_complete'),
]
urlpatterns = [
    re_path(r'^$', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False)),
    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='user/login.html', authentication_form=AuthenticationForm), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='user/logout.html', extra_context={'form':AuthenticationForm}),name ='logout'),
    path('disable_account/', DisableUserAccount.as_view(), name='disable_account'),
    path('signup/', SingUpView.as_view(), name='signup'),
    path('<str:username>/',UserProfile.as_view(),name='profile'),
    path('password/',include(password_urlpatterns)),
]


