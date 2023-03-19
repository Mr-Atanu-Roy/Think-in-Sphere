from django.urls import path
from .views import *

urlpatterns = [
   path('create/<topic>', createExam, name="create-exam"),
   path('give-exam/<exam_id>', giveExam, name="give-exam"),
   path('result/<exam_id>', examResult, name="exam-result"),
]
