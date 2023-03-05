from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from core.models import ChatRoom, UserRequestHistory

from core.utils import Speak, random_name

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
    query = result = ""
    context = {
        "query" : query,
        "result" : result,
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
            if query == "":
                message = "Please input some text"
                messages.error(request, message)
                result = message
                
            else:
                if getRoom:
                    if cache.get(query):
                        result = cache.get(query)                
                    else:
                        prompt = f"The following is a conversation of a student with an AI assistant. The assistant is helpful, creative, clever, and very friendly and answers all the questions of the student very clearly.\n\nHuman: {query}\n\nAI:"
                                    
                        response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=2048,
                        temperature=0.9,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        stop=[" Human:", " AI:"]
                        )
                        
                        result =  response["choices"][0]["text"]
                        result = result.lstrip()
                        cache.set(query, result) 
                        
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
                if query == "":
                    message = "Please say something"
                    messages.error(request, message)
                    result = message
                else:
                    if getRoom:
                        if cache.get(query):
                            result = cache.get(query)
                        else:
                            prompt = f"The following is a conversation of a student with an AI assistant. The assistant is helpful, creative, clever, and very friendly and answers all the questions of the student very clearly.\n\nHuman: {query}\n\nAI:"
                                
                            response = openai.Completion.create(
                            model="text-davinci-003",
                            prompt=prompt,
                            max_tokens=2048,
                            temperature=0.9,
                            top_p=1,
                            frequency_penalty=0.0,
                            presence_penalty=0.6,
                            stop=[" Human:", " AI:"]
                            )

                            result =  response["choices"][0]["text"]
                            result = result.lstrip()
                            cache.set(query, result)
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
    
    Speak(result).start()
    
    return render(request, './core/chat.html', context)


@login_required(login_url="/auth/login")
def course(request):
    
    return render(request, './core/course.html')


@login_required(login_url="/auth/login")
def courseSearch(request, course):
    
    return render(request, './core/view-course.html')



