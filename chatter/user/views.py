from django.shortcuts import render
from .forms import SignUpForm, ProfileForm
from .models import Profile
from django.contrib.auth import get_user, logout
from django.conf import settings
from django.views import View




