from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from accounts.utils import current_time
from core.models import UserRequestHistory
from course.models import UserCourseHistory
import datetime
from django.db.models import Count
from django.contrib.humanize.templatetags.humanize import naturalday
from django.template.defaultfilters import truncatewords

from .utils import courses_list
# Create your views here.

class DashboardDashboardSearchQueryView(View):
    '''Handels dashboard search ajax request'''
    
    def get(self, request):
        try:
            query = request.GET.get('query')
            if query:
                if query.isspace() == False:
                    last_week = current_time - datetime.timedelta(days=7)
                    
                    #getting chat history
                    result1 = UserRequestHistory.objects.filter(chatroom__user=request.user, created_at__gte=last_week, request__icontains=query)
                    #getting course
                    result2 = UserCourseHistory.objects.filter(user=request.user, created_at__gte=last_week, request__icontains=query)

                    data1 = [{'id': obj.id, 'request': truncatewords(obj.request, 13), 'created_at' : naturalday(obj.created_at)} for obj in result1]
                    data2 = [{'id': obj.id, 'request': truncatewords(obj.request, 13), 'created_at' : naturalday(obj.created_at)} for obj in result2]
                    
                    data =  sorted(data1 + data2, key=lambda x: x['created_at'], reverse=True)
                    
                    return JsonResponse(data, safe=False)
                
                
                return JsonResponse("", safe=False)
            
        except Exception as e:
            print(e)
        
class CourseSerchQueryView(View):
    '''handels course search ajax request'''
    
    def get(self, request):
        try:
            query = request.GET.get('query')
            if query:
                if query.isspace() == False:
                    similar_course = []
                    for course in courses_list:
                        if query.lower() in course.lower():
                            similar_course.append(course.title())
                    
                    return JsonResponse({"data": similar_course})
                
            return JsonResponse("", safe=False)
            
        except Exception as e:
            print(e)   