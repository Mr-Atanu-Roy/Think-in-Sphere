from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name="home"),
    
    path('chat/room/', chatRooms, name="chat-rooms"),
    path('chat/room/create', createRoom, name="create-room"),
    path('chat/room/<room_id>', chat, name="chat"),

]
