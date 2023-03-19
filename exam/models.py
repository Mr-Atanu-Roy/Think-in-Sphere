from django.db import models
from accounts.models import User
from accounts.utils import BaseModel

import uuid

exam_status_choices = (
    ('given', 'Given'),
    ('not-given', 'Not Given'),
)

# Create your models here.
class ExamDetails(BaseModel):
    
    exam_id = models.UUIDField(default=uuid.uuid4, verbose_name="Exam ID", editable=False, unique=True)
    exam_name = models.CharField(max_length=400, blank=True)
    no_questions = models.IntegerField(default=0)
    corrected_questions = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_topic = models.CharField(max_length=255)
    exam_marks = models.IntegerField()
    user_marks = models.IntegerField(default=0)
    exam_time = models.IntegerField()
    time_taken = models.IntegerField(default=0)
    exam_status = models.CharField(choices=exam_status_choices, max_length=255, default='not-given')
    appearence = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Exam Details"
        ordering = ['created_at']
    
    def __str__(self):
        return self.exam_name
    
    
class ObjectiveExamQuestions(BaseModel):
    
    question_id = models.CharField(max_length=255, verbose_name="Question ID", editable=False, unique=True)
    exam = models.ForeignKey(ExamDetails, on_delete=models.CASCADE)
    question = models.TextField()
    opt1 = models.CharField(max_length=500)
    opt2 = models.CharField(max_length=500)
    opt3 = models.CharField(max_length=500)
    opt4 = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    user_answer = models.CharField(max_length=500, default="not-answered")

    class Meta:
        verbose_name_plural = "Exam-Objective Questions"
        ordering = ['created_at']
    
    def __str__(self):
        return self.question_id
    
    
    