from django.contrib import admin
from .models import RoomCategory, ChatRoom, PrivateChatRoom

admin.site.register(RoomCategory)
admin.site.register(ChatRoom)
admin.site.register(PrivateChatRoom)
