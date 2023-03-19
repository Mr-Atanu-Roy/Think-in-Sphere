from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ExamDetails, ObjectiveExamQuestions

from core.utils import openai_general_endpoint

import random, uuid

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.


@login_required(login_url="/auth/login")
def createExam(request, topic):
    no_questions = 10
    exam_marks = no_questions*1
    exam_time = no_questions*1.5
    exam_name = f"{topic.capitalize()} Test {random.randint(10, 100000)}"
    context = {}
    try:
        if request.method == "POST":
            no_questions = int(request.POST.get('no_questions'))
            exam_name = request.POST.get('exam_name')
            exam_marks = no_questions*1
            exam_time = no_questions*1.5
            
            if exam_name != "":
                newExam = ExamDetails(user=request.user, exam_name = exam_name, exam_topic=topic.lower(), exam_marks=exam_marks, exam_time=exam_time, no_questions=no_questions)
                newExam.save()
                
                return redirect(f"/exam/give-exam/{newExam.exam_id}")
            else:
                messages.error(request, "Please give some exam name")
    
    except Exception as e:
        print(e)
        
        
    context["no_questions"] = no_questions
    context["topic"] = topic
    context["exam_name"] = exam_name
    context["exam_marks"] = exam_marks
    context["exam_time"] = exam_time
    
    return render(request, './exam/create_exam.html', context)



@login_required(login_url="/auth/login")
def giveExam(request, exam_id):
    context = {}
    questions_dict = {}
    try:
        try:
            getExam = ExamDetails.objects.get(exam_id=exam_id)
            exam_topic = getExam.exam_topic
            no_questions = getExam.no_questions
        except ExamDetails.DoesNotExist:
            messages.warning("Invalid URL")
            return redirect('dashboard')
        except Exception as e:
            print(e)
        
        
        if request.method == "POST":
            for result in request.POST:
                try:
                    get_question = ObjectiveExamQuestions.objects.get(question_id=result)
                    get_question.user_answer = request.POST.get(result)
                    get_question.save()
                    return redirect(f'exam/result/{exam_id}')
                except Exception as e:
                    print(e)                
        
        # check_question = ObjectiveExamQuestions.objects.filter(exam=getExam)
        
        # if len(check_question) > 0:
        #     for question in check_question:
        #         question_id = question.question_id
        #         question = question.question
        #         opt1 = question.opt1
        #         opt2 = question.opt2
        #         opt3 = question.opt3
        #         opt4 = question.opt4
                
        #         questions_dict[question_id] = {
        #             "question" : question,
        #             # "opt1" : opt1,
        #             # "opt2" : opt2,
        #             # "opt3" : opt3,
        #             # "opt4" : opt4,
        #         }
                
        # else:
        if cache.get(f"exam-{exam_id}"):
            questions_dict = cache.get(f"exam-{exam_id}")
        else:
            if no_questions > 12:
                token = 3500
                temprature = 0.8
            else:
                token = 2200
                temprature = 0.68
            prompt = f"Generate {no_questions} questions on topic {exam_topic} in format question:\noption1:\noption2:\noption3:\noption4:\nanswer:\n\n question:\noption1:\noption2:\noption3:\noption4:\nanswer:\n\nquestion:"
            response = openai_general_endpoint(prompt, token=token, temperature=temprature).lower()
            lines = response.split('\n\n')
            for questions in lines:
                newLines = questions.split('\n')
                question = (newLines[0].replace('question:', '')).strip()
                if "answer:" in newLines[1].lower():
                    answer = (newLines[1].replace('answer: ', '')).strip()
                    opt1 = (newLines[2].replace('option1: ', '')).strip()
                    opt2 = (newLines[3].replace('option2: ', '')).strip()
                    opt3 = (newLines[4].replace('option3: ', '')).strip()
                    opt4 = (newLines[5].replace('option4: ', '')).strip()
                else:
                    opt1 = (newLines[1].replace('option1: ', '')).strip()
                    opt2 = (newLines[2].replace('option2: ', '')).strip()
                    opt3 = (newLines[3].replace('option3: ', '')).strip()
                    opt4 = (newLines[4].replace('option4: ', '')).strip()
                    answer = (newLines[5].replace('answer: ', '')).strip()
                
                question_id = str(uuid.uuid4())
                
                newQuestion = ObjectiveExamQuestions(exam=getExam, question_id=question_id, question=question, opt1=opt1, opt2=opt2, opt3=opt3, opt4=opt4, correct_answer = answer)
                newQuestion.save()
                
                questions_dict[question_id] = {
                    "question" : question,
                    "opt1" : opt1,
                    "opt2" : opt2,
                    "opt3" : opt3,
                    "opt4" : opt4,
                }
            
            cache.set(f"exam-{exam_id}", questions_dict)
                
    
        context["exam_name"] = getExam.exam_name
        context["exam_topic"] = exam_topic
        context["exam_marks"] = getExam.exam_marks
        context["exam_time"] = getExam.exam_time
        context["no_questions"] = no_questions
        context["questions"] = questions_dict
        
    except Exception as e:
        print(e)
        
    return render(request, './exam/give_exam.html', context)




@login_required(login_url="/auth/login")
def examResult(request, exam_id):
    context = {}



    return render(request, './exam/exam_result.html', context)


