from django.contrib import admin
from .models import Profile
from django.db.models import Count,OuterRef,Subquery
from django.contrib.auth.models import User



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Class to construct a custom admin model for Profile model'''

    list_display = ('username', 'name', 'email_confirmed')
    list_filter = ('email_confirmed', )
    search_fields = ('username', )



