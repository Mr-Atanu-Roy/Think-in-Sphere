from core.models import ChatRoom

def my_context(request):
    room = ChatRoom.objects.last()

    context = {
        "user_fname" : request.user.first_name,
        "last_room_id" : room.room_id,
        "last_room_url" : f"/chat/room/{room.room_id}",
    }
    
    return context