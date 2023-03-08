from django.contrib import admin
from .models import *

# Register your models here.

class UserCourseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'request', 'type', 'created_at')
    fieldsets = [
        ("Details", {
            "fields": (
                ['user', 'request', 'type']
            ),
        }),
    ]
    
    search_fields = ["user", "request", "type"]


#registering UserCourseHistory model
admin.site.register(UserCourseHistory, UserCourseHistoryAdmin)
