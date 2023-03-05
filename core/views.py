from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from core.models import ChatRoom, UserRequestHistory

from core.utils import Speak, random_name, openai_completion_endpoint, openai_image_endpoint

import openai
import speech_recognition as sr

import os
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Load OPENAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")



# Create your views here.

def home(request):
    return render(request, './core/home.html')


@login_required(login_url="/auth/login")
def chatRooms(request):
    chatRooms = ChatRoom.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        "chatRooms" : chatRooms,
    }
    

    return render(request, './core/view-chatrooms.html', context)


@login_required(login_url="/auth/login")
def createRoom(request):
    room_name = random_name()
    context = {
        "room_name" : room_name,
    }
    
    try:
        if request.method == "POST":
            room_name = request.POST.get('room_name')
            
            if room_name != "":
                if len(room_name) > 10:
                    newRoom = ChatRoom(user=request.user, room_name=room_name)
                    newRoom.save()
                    
                    return redirect(f'/chat/room/{newRoom.room_id}')
                else:
                    messages.error(request, "Room name too small")
            else:
                messages.error(request, "Room name is required")
        
    except Exception as e:
        print(e)
        
    context["room_name"] = room_name
    
    return render(request, './core/create-room.html', context)


@login_required(login_url="/auth/login")
def chat(request, room_id):
    query = result = imgResult = ""
    context = {
        "query" : query,
        "result" : result,
        "imgResult" : imgResult,
    }
    
    chatRooms = ChatRoom.objects.filter(user=request.user).order_by('-created_at')
    context["chatRooms"] = chatRooms
    try:
        getRoom = ChatRoom.objects.get(room_id=room_id)
        chats = UserRequestHistory.objects.filter(chatroom=getRoom)
        context["room_name"] = getRoom.room_name
        context["chats"] = chats
        
    except Exception as e:
        print(e)
        
        
    try:
        if request.method == "POST" and "text-input" in request.POST:
            query = request.POST.get("query")
            query = query.lower()
            if query.isspace():
                message = "Please input some text"
                messages.error(request, message)
                result = message
                
            else:
                if getRoom:
                    if cache.get(query):
                        result = cache.get(query).get("text")    
                        imgResult = cache.get(query).get("img")
                                  
                    else:
                        result = openai_completion_endpoint(query)
                        imgResult = openai_image_endpoint(result[0:100])
                        
                        cache_dict = {
                            "text" : result,
                            "img" : imgResult
                        } 
                        
                        cache.set(query, cache_dict)   
                        
                    newChat = UserRequestHistory(request=query, response=result)  
                    newChat.save() 
                    newChat.chatroom.add(getRoom)
                    newChat.save()
                else:
                    print("No room selected")
                    messages.error(request, "No room selected")

        elif request.method == "POST" and "voice-input" in request.POST:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            # recognize speech using Google Speech Recognition
            try:
                query = r.recognize_google(audio)
                query = query.lower()
                if query.isspace():
                    message = "Please say something"
                    messages.error(request, message)
                    result = message
                else:
                    if getRoom:
                        if cache.get(query):
                            result = cache.get(query).get("text")    
                            imgResult = cache.get(query).get("img")
                                  
                        else:
                            result = openai_completion_endpoint(query)
                            imgResult = openai_image_endpoint(result[0:100])
                            
                            cache_dict = {
                                "text" : result,
                                "img" : imgResult
                            } 
                            
                            cache.set(query, cache_dict)   
                    else:
                        print("No room selected")
                        messages.error(request, "No room selected")
                    
                    newChat = UserRequestHistory(request=query, response=result)  
                    newChat.save() 
                    newChat.chatroom.add(getRoom)
                    newChat.save()
                
            except sr.UnknownValueError:
                result = "I could not understand what you just said. Please say that again"
            except sr.RequestError as e:
                result = "Could not request results from Google Speech Recognition service; {0}".format(e)
    
    except Exception as e:
        print(e)
    
    context["query"] = query
    context["result"] = result
    context["imgResult"] = imgResult
    
    Speak(result).start()
    
    return render(request, './core/chat.html', context)



