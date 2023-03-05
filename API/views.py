from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from accounts.utils import current_time
from core.models import UserRequestHistory
import datetime

from django.contrib.humanize.templatetags.humanize import naturalday
from django.template.defaultfilters import truncatewords

from .utils import courses_list
# Create your views here.

class DashboardSearchQueryView(View):
    '''Handels dashboard search ajax request'''
    
    def get(self, request):
        try:
            query = request.GET.get('query')
            
            if query.isspace() == False:
                last_month = current_time - datetime.timedelta(days=30)
                result = UserRequestHistory.objects.filter(chatroom__user=request.user, created_at__gte=last_month, request__icontains=query).order_by('-created_at')
            
                data = [{'id': obj.id, 'request': truncatewords(obj.request, 13), 'created_at' : naturalday(obj.created_at)} for obj in result]
                return JsonResponse(data, safe=False)
            
            return JsonResponse("", safe=False)
            
        except Exception as e:
            print(e)
        
class CourseSerchQueryView(View):
    '''handels course search ajax request'''
    
    def get(self, request):
        try:
            query = request.GET.get('query')
            if query.isspace() == False:
                similar_course = []
                for course in courses_list:
                    if query.lower() in course.lower():
                        similar_course.append(course.title())
                
                return JsonResponse({"data": similar_course})
                
            return JsonResponse("", safe=False)
            
        except Exception as e:
            print(e)   