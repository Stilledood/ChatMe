from django.urls import re_path, path,include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .views import UserProfile
from django.urls import reverse_lazy


app_name='user'

password_urlpatterns = [
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='user/change_password.html',success_url=reverse_lazy('dj-auth:password_change_done')),name='password_change'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html', extra_context ={'form':AuthenticationForm}),name='password_change_done')
]
urlpatterns = [
    re_path(r'^$', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False)),
    re_path(r'^login/$',auth_views.LoginView.as_view(template_name='user/login.html', authentication_form=AuthenticationForm), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='user/logout.html', extra_context={'form':AuthenticationForm}),name ='logout'),
    re_path(r'^(?P<username>[\w\-]+)/$',UserProfile.as_view(),name='profile'),
    path('password/',include(password_urlpatterns)),

]


