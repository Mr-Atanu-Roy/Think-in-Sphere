from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import ChatRoom, UserRequestHistory
from accounts.models import UserProfile

from core.utils import Speak, random_name, openai_completion_endpoint, openai_image_endpoint, detect_language, translate_text

import speech_recognition as sr

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



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
    lang_code = "en"
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
            if query == "":
                message = "Please input some text"
                messages.error(request, message)
                result = message
                
            else:
                if getRoom:
                    if cache.get(query):
                        result = cache.get(query).get("text")    
                        imgResult = cache.get(query).get("img")
                        lang_code = cache.get(query).get("lang_code")
                                  
                    else:
                        lang_code, lang, err = detect_language(query)   #detect the lang of input query
                        if err == None:
                            
                            if lang_code == "en":           #if lang is english then don't translate it
                                translated_text, err1 = query, None
                            else:                           #else translate it
                                translated_text, err1 = translate_text(query, lang_code, 'en')  #translate it to english
                            
                            if err1 == None:
                                result = openai_completion_endpoint(translated_text)    #send request to openai(in english) and get response(in english)
                                
                                if "hello" in query.lower() or "hi" in query or  "hi there" in result.lower() or "i help you" in result.lower():
                                    imgResult = ""
                                else:
                                    imgResult = openai_image_endpoint(result[0:100])    #send request to dalle(in english)
                                
                                if lang_code != "en":       #translate if lang is not english
                                    result, err2 = translate_text(result, 'en', lang_code)    #translate the response back to the input lang
                                else:
                                    err2 = None
                                    
                                if err2 == None:
                                    
                                    cache_dict = {
                                        "text" : result,   
                                        "img" : imgResult,
                                        "lang_code" : lang_code
                                    } 
                                    cache.set(query, cache_dict)  #set the cache
                                
                                    #save data to db
                                    newChat = UserRequestHistory(request=query, response=result)  
                                    newChat.save() 
                                    newChat.chatroom.add(getRoom)
                                    newChat.save()
                                else:
                                    message.error(request, "Some thing went wrong. Please try again")
                            else:
                                message.error(request, "Some thing went wrong. Please try again")
                        else:
                            message.error(request, "Some thing went wrong. Please try again")
                                                
                                             
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
                user_profile = UserProfile.objects.filter(user=request.user).first()
                lang_code_recog = user_profile.language+'-IN'
                query = r.recognize_google(audio, language=lang_code_recog)
                print(query)
                # query = query.lower()
                if query == "":
                    message = "Please say something"
                    messages.error(request, message)
                    result = message
                else:
                    if getRoom:
                        if cache.get(query):
                            result = cache.get(query).get("text")    
                            imgResult = cache.get(query).get("img")
                            lang_code = cache.get(query).get("lang_code")
                                  
                        else:
                            lang_code, lang, err = detect_language(query)   #detect the lang of input query
                            if err == None:
                                
                                if lang_code == "en":    #if lang is english then don't translate it
                                    translated_text, err1 = query, None
                                else:                    #else translate it
                                    translated_text, err1 = translate_text(query, lang_code, 'en')  #translate it to english
                                
                                if err1 == None:
                                    result = openai_completion_endpoint(translated_text)    #send request to openai(in english) and get response(in english)
                                    
                                    if "hello" in query.lower() or "hi" in query or  "hi there" in result.lower() or "i help you" in result.lower():
                                        imgResult = ""
                                    else:
                                        imgResult = openai_image_endpoint(result[0:100])    #send request to dalle(in english)
                                    
                                    if lang_code != "en":       #translate if lang is not english
                                        result, err2 = translate_text(result, 'en', lang_code)    #translate the response back to the input lang
                                    else:
                                        err2 = None
                                        
                                    if err2 == None:
                                        
                                        cache_dict = {
                                            "text" : result,   
                                            "img" : imgResult,
                                            "lang_code" : lang_code
                                        } 
                                        cache.set(query, cache_dict)  #set the cache

                                        #save data to db
                                        newChat = UserRequestHistory(request=query, response=result)  
                                        newChat.save() 
                                        newChat.chatroom.add(getRoom)
                                        newChat.save()
                                        
                                    else:
                                        message.error(request, "something went wront. Please try again")
                                else:
                                    message.error(request, "something went wront. Please try again")
                            else:
                                message.error(request, "something went wront. Please try again")
                    else:
                        print("No room selected")
                        messages.error(request, "No room selected")
                    
                
            except sr.UnknownValueError:
                result = "I could not understand what you just said. Please say that again"
            except sr.RequestError as e:
                result = "Could not request results from Google Speech Recognition service; {0}".format(e)
       
    except Exception as e:
        print(e)
    
    context["query"] = query
    context["result"] = result
    context["imgResult"] = imgResult
    
    if result != "":
        Speak(result, lang_code).start()
    
    return render(request, './core/chat.html', context)



