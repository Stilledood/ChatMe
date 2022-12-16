from django.contrib import admin
from .models import RoomCategory, ChatRoom, PrivateChatRoom
from django.db.models import Count

admin.site.register(RoomCategory)
admin.site.register(PrivateChatRoom)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    '''Class to create a custom admin model for ChatRoom '''

    date_hierarchy = 'date_created'
    list_display = ('name', 'room_owner', 'category', 'date_created', 'admin_created_room', 'online_members' )
    list_filter = ('date_created', 'room_owner')
    search_fields = ('name', )
    fieldsets = (
        (None,{
            'fields':('name', 'room_owner', 'room_image', 'admin_created_room')
        }),
        ('Related',{
            'fields':('online', 'category')
        })
    )
    filter_horizontal = ('online', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(members = Count('online'))
    def online_members(self,chatroom):
        return chatroom.members
    online_members.short_description = 'Members'
    





