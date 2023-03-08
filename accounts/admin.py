from django.contrib import admin
from .models import *
from core.models import ChatRoom
from course.models import UserCourseHistory

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = UserProfile
    
class ChatRoomInline(admin.StackedInline):
    model = ChatRoom
    extra = 0
    

class UserCourseHistoryInline(admin.StackedInline):
    model = UserCourseHistory    
    extra = 0
    

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'is_staff', 'last_login')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['is_verified', 'date_joined', 'last_login', 'last_logout']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ),
        }),
    ]
    
    inlines = [ProfileInline, ChatRoomInline, UserCourseHistoryInline]
    
    search_fields = ["email", "first_name", "last_name", "is_verified"]
    
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'created_at')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['user', 'country', 'city', 'date_of_birth']
            ),
        }),
        ("More Details", {
            "fields": (
                ['course_name', 'institute_name']
            ),
        }),
        ("User's Prompt For Chatbot ", {
            "fields": (
                ['bot_prompt']
            ), 'classes': ['collapse']
        }),
    ]

    
    search_fields = ["user", "country"]
    
    
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp', 'user', 'purpose', 'is_expired', 'created_at')
    fieldsets = [
        ("OTP Details", {
            "fields": (
                ['user', 'purpose', 'is_expired', 'otp']
            ),
        }),
    ]
    
    search_fields = ["user", "is_expired"]


#registering User model
admin.site.register(User, UserAdmin)

#registering profile model
admin.site.register(UserProfile, UserProfileAdmin)

#registering otp model
admin.site.register(OTP, OTPAdmin)