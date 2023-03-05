from django.contrib import admin
from .models import *

# Register your models here.

class UserRequestHistoryInline(admin.StackedInline):
    model = UserRequestHistory
    

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_id', 'user', 'created_at')
    fieldsets = [
        ("Chat Room Details", {
            "fields": (
                ['room_name', 'user']
            ),
        }),
    ]
    
    search_fields = ["room_name", "user"]
    
class UserRequestHistoryAdmin(admin.ModelAdmin):
    list_display = ('request', 'response', 'created_at')
    fieldsets = [
        ("Details", {
            "fields": (
                ['request', 'response', 'chatroom']
            ),
        }),
    ]
    
    search_fields = ["request", "response"]
    
    
#registering chatroom model
admin.site.register(ChatRoom, ChatRoomAdmin)

#registering UserRequestHistory model
admin.site.register(UserRequestHistory, UserRequestHistoryAdmin)