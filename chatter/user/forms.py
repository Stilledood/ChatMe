from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from django import forms



class SignUpForm(UserCreationForm):
    '''Class to create a form for sign up process'''

    first_name = forms.CharField(max_length=128, required=False, help_text='optional')
    last_name = forms.CharField(max_length=128, required=False, help_text='optional')
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    '''Class to construnct a form to update profile informations'''

    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control', 'type':'file', 'id':'image'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'id':'name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'id':'username'}))

    class Meta:
        model = Profile
        fields = ['image', 'name', 'username']
