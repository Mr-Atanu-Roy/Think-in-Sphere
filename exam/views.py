from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ExamDetails, ObjectiveExamQuestions
from accounts.models import UserProfile

from core.utils import openai_general_endpoint, detect_language, translate_text

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
    lang_code = 'en'
    try:
        try:
            getProfile = UserProfile.objects.get(user=request.user)
            lang_code = getProfile.language
        except ExamDetails.DoesNotExist:
            messages.warning("Invalid User")
            return redirect('home')
        except Exception as e:
            print(e)
            
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
            for key in request.POST:
                if key.lower() != "csrfmiddlewaretoken":
                    if lang_code != "en":
                        result, err = translate_text(request.POST.get(key), lang_code, 'en')
                        if err == None:
                            try:
                                get_question = ObjectiveExamQuestions.objects.get(question_id=key)
                                get_question.user_answer = result.lower()
                                get_question.save()
                                if (get_question.correct_answer).lower() == result.lower():
                                    getExam.user_marks += 1
                                    getExam.save()
                                return redirect(f'/exam/result/{exam_id}')
                            except Exception as e:
                                print(e)                
        
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
                
                if lang_code != "en":
                    translated_question, err1 = translate_text(question, 'en', lang_code)
                    if err1 == None:
                        question = translated_question
                        
                    translated_opt1, err2 = translate_text(opt1, 'en', lang_code)
                    if err2 == None:
                        opt1 = translated_opt1
                        
                    translated_opt2, err3 = translate_text(opt2, 'en', lang_code)
                    if err3 == None:
                        opt2 = translated_opt2
                        
                    translated_opt3, err4 = translate_text(opt3, 'en', lang_code)
                    if err4 == None:
                        opt3 = translated_opt3
                        
                    translated_opt4, err5 = translate_text(opt4, 'en', lang_code)
                    if err5 == None:
                        opt4 = translated_opt4
                        
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
    getExam = getQuestions = ""
    user_percent = 0
    
    try:
        getExam = ExamDetails.objects.get(exam_id=exam_id)
        user_percent = (getExam.user_marks/getExam.exam_marks)*100
        if getExam:
            getQuestions = ObjectiveExamQuestions.objects.filter(exam=getExam)
        
    except Exception as e:
        messages.error(request, "Something went wrong")
        print(e)
        

    context["get_exam"] = getExam
    context["get_questions"] = getQuestions
    context["user_percent"] = round(user_percent, 2)
    
    return render(request, './exam/exam_result.html', context)


