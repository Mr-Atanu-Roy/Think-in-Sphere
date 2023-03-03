from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name="home"),
    
    path('chat-rooms/', chatRooms, name="chat-rooms"),
    path('chat/room/<room_id>', chat, name="chat"),
    
    path('course/', course, name="course"),
    path('course/<course>', courseSearch, name="view-course"),
]
