from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.utils import check_str_special
from core.utils import openai_general_endpoint, translate_text
from .utils import generate_content

from accounts.models import UserProfile
from .models import UserCourseHistory

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

@login_required(login_url="/auth/login")
def course(request):
    course_search = ""
    user_lang = "en"
    context = {
        "course_search" : course_search
    }
    
    try:
        user = UserProfile.objects.get(user=request.user)
        user_lang = user.language

        if request.method == "POST":
            course_search = request.POST.get("course-search")
            if not course_search.isspace():
                if check_str_special(course_search):
                    messages.error(request, "Invalid course name")
                else:
                    url = f"/course/view/{course_search}"
                    return redirect(url)
            else:
                messages.error(request, "You must input some course name")
    except Exception as e:
        print(e)
    
    context["course_search"] = course_search
    context["user_lang"] = user_lang
    return render(request, './course/course.html', context)


@login_required(login_url="/auth/login")
def courseSearch(request, course):
    topic_search = result = ""
    user_lang = "en"
    context = {}
    
    try:
        user = UserProfile.objects.get(user=request.user)
        user_lang = user.language
        
        if course != "":
            prompt = f"Generate 10 to 15 subtopics for course {course}"
            prompt = prompt.lower().strip()
            if cache.get(prompt):
                result = cache.get(prompt)
            else:
                response = openai_general_endpoint(prompt, token=700, temperature=0.5)
                    
                result = {}
                lines = response.split("\n")
                for line in lines:
                    parts = line.split('. ')
                    key = parts[1]
                    
                    if user_lang != "en":
                        translated_text, err = translate_text(key, 'en', user_lang)
                        if err != None:
                            translated_text = key
                    else:
                        translated_text = key
                    
                    value = translated_text
                    result[key] = value
                
                cache.set(prompt, result)
            
            newHistory = UserCourseHistory(user=request.user, request=f"{course}")
            newHistory.save()
    
        if request.method=="POST":
            topic_search = request.POST.get("topic-search")
            detect_lang, _, error = detect_lang(topic_search)
            
            if error == None and user_lang != "en":
                topic_search, err1 = translate_text(topic_search, detect_lang, 'en')
                    
            if topic_search != "":
                if check_str_special(topic_search):
                    messages.error(request, "Invalid course name")
                else:
                    url = f"/course/view/topic/{topic_search.lower()} in {course.lower()}"
                    print(url)
                    return redirect(url)
            else:
                messages.error(request, "You must input some course name")
            
            
    except Exception as e:
        print(e)
    
    context["course"] = course
    context["result"] = result
    context["topic_search"] = topic_search
    context["user_lang"] = user_lang
    
    return render(request, './course/view-course.html', context)


@login_required(login_url="/auth/login")
def courseTopicView(request, topic):
    notes = summery = question = ""
    user_lang = "en"
    context = {}
    
    try:
        user = UserProfile.objects.get(user=request.user)
        user_lang = user.language
        
        if not topic.isspace():

            if cache.get(topic):
                notes, summery, question = cache.get(topic)["notes"], cache.get(topic)["summery"], cache.get(topic)["question"]
                
            else:
                notes1, summery1, question1 = generate_content(topic)
                if user_lang != "en":
                    notes, err1 = translate_text(notes1, "en", user_lang)
                    summery, err2 = translate_text(summery1, "en", user_lang)
                    question, err3 = translate_text(question1, "en", user_lang)
                    if err1 != None:
                        notes = notes1
                    if err2 != None:
                        summery = summery1
                    if err3 != None:
                        question = question1
                else:
                    notes = notes1
                    summery = summery1
                    question = question1
                    
                    
                cache_dict = {
                    "notes" : notes,
                    "summery" : summery,
                    "question" : question,
                }
                cache.set(topic, cache_dict)
                
        topic = topic.lower()
        newTopic = UserCourseHistory(user=request.user, request=topic, type="topic")
        newTopic.save()
                
    except Exception as e:
        print(e)
        
    context["topic"] = topic
    context["user_lang"] = user_lang
    context["notes"] = notes
    context["summery"] = summery
    context["question"] = question
    
    return render(request, './course/course-topic.html', context)

