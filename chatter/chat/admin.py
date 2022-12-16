from django.contrib import admin
from .models import RoomCategory, ChatRoom, PrivateChatRoom
from django.db.models import Count

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


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    '''Class to create a custom admin model for RoomCategory model'''

    list_display = ('name', 'slug', 'room_number')
    list_filter = ('name', 'slug')
    search_fields = ('name',)


    def room_number(self,category):
        return category.chatroom_set.count()
    room_number.short_description = 'Rooms'



