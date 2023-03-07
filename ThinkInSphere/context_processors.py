from core.models import ChatRoom

def my_context(request):
    context = {
        "user_fname" : "Anonymus",
        "user_email" : "anonymus@example.com",
    }
    try:
        if request.user.is_authenticated:
            fname = request.user.first_name
            email = request.user.email
            
            context["user_fname"] = fname
            context["user_email"] = email
            
            room = ChatRoom.objects.filter(user=request.user).last()

            if room is not None:
                last_room_id = room.room_id
                last_room_url = f"/chat/room/{room.room_id}"
            
                context["last_room_id"] = last_room_id
                context["last_room_url"] = last_room_url
    except Exception as e:
        print(e)

    
    return context