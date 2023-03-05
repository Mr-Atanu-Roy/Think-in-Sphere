from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from accounts.utils import current_time
from core.models import UserRequestHistory
import datetime

from django.contrib.humanize.templatetags.humanize import naturalday
# Create your views here.

class SearchQueryView(View):
    '''Handels ajax request'''
    
    def get(self, request):
        try:
            query = request.GET.get('query')
            
            if query.isspace() == False:
                last_month = current_time - datetime.timedelta(days=30)
                result = UserRequestHistory.objects.filter(chatroom__user=request.user, created_at__gte=last_month, request__icontains=query).order_by('-created_at')
            
                data = [{'id': obj.id, 'request': obj.request[0:45], 'created_at' : naturalday(obj.created_at)} for obj in result]
                return JsonResponse(data, safe=False)
            
            return JsonResponse("", safe=False)
            
        except Exception as e:
            print(e)
        