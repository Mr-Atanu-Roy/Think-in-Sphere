from django.contrib import admin
from .models import ExamDetails, ObjectiveExamQuestions

# Register your models here.

class ExamQuestionInline(admin.StackedInline):
    model = ObjectiveExamQuestions
    extra = 0
    

class ExamDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam_name', 'exam_topic', 'exam_marks', 'user_marks', 'exam_time', 'created_at')
    fieldsets = [
        ("Exam Details", {
            "fields": (
                ['exam_name', 'exam_topic', 'no_questions', 'exam_marks', 'exam_time']
            ),
        }),
        ("User Details", {
            "fields": (
                ['user', 'user_marks', 'time_taken', 'corrected_questions']
            ),
        }),
    ]
    
    inlines = [ExamQuestionInline]
    search_fields = ["exam_topic", "user"]
    
    
class ObjectiveExamQuestionsAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'created_at')
    fieldsets = [
        ("Exam Details", {
            "fields": (
                ['exam', 'question']
            ),
        }),
        ("Option Details", {
            "fields": (
                ['opt1', 'opt2', 'opt3', 'opt4']
            ),
        }),
        ("Answer Details", {
            "fields": (
                ['correct_answer', 'user_answer']
            ),
        }),
    ]
    
    search_fields = ["exam", "question", "correct_answer"]

    
    
#registering ExamDetails model
admin.site.register(ExamDetails, ExamDetailsAdmin)

#registering ObjectiveExamQuestions model
admin.site.register(ObjectiveExamQuestions, ObjectiveExamQuestionsAdmin)

