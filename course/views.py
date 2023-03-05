from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.utils import check_str_special
from core.utils import openai_general_endpoint
from .utils import generate_content

from .models import UserCourseHistory

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

@login_required(login_url="/auth/login")
def course(request):
    course_search = ""
    context = {
        "course_search" : course_search
    }
    
    try:
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
    return render(request, './course/course.html')


@login_required(login_url="/auth/login")
def courseSearch(request, course):
    topic_search = result = ""
    context = {}
    
    try:
        if not course.isspace():
            prompt = f"Generate 10 to 15 subtopics for course {course}"
            prompt = prompt.lower().strip()
            if cache.get(prompt):
                result = cache.get(prompt)
            else:
                result = openai_general_endpoint(prompt, token=700, temperature=0.5)
                result = [line.split(". ", 1)[1] for line in result.split("\n")]
                
                cache.set(prompt, result)
            
            newHistory = UserCourseHistory(user=request.user, request=f"{course}")
            newHistory.save()
    
        if request.method=="POST":
            topic_search = request.POST.get("topic-search")
            
            if not topic_search.isspace():
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
    
    return render(request, './course/view-course.html', context)


@login_required(login_url="/auth/login")
def courseTopicView(request, topic):
    notes = summery = question = ""
    context = {}
    
    try:
        if not topic.isspace():
            topic = topic.lower()

            if cache.get(topic):
                notes, summery, question = cache.get(topic)["notes"], cache.get(topic)["summery"], cache.get(topic)["question"]
                
            else:
                notes, summery, question = generate_content(topic)
                cache_dict = {
                    "notes" : notes,
                    "summery" : summery,
                    "question" : question,
                }
                cache.set(topic, cache_dict)
                
    except Exception as e:
        print(e)
        
    context["topic"] = topic
    context["notes"] = notes
    context["summery"] = summery
    context["question"] = question
    
    return render(request, './course/course-topic.html', context)

