from django.urls import path
from .views import *

urlpatterns = [
   path('', course, name="course"),
   path('view/<course>', courseSearch, name="view-course"),
   path('view/topic/<topic>', courseTopicView, name="view-course-topic"),
]
