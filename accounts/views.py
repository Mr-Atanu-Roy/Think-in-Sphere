from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import os
import datetime

import os
import datetime

from core.models import UserRequestHistory
from course.models import UserCourseHistory
from accounts.models import User, OTP, UserProfile
from core.models import UserRequestHistory
from django.db.models import Count

from accounts.utils import current_time, check_recaptcha, check_str_special

RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")


# Create your views here.
@check_recaptcha
def signin(request):
    context = {
        "RECAPTCHA_PUBLIC_KEY" : RECAPTCHA_PUBLIC_KEY,
        "fname": "",
        "lname": "",
        "email": "",
        "dob": "",
        "password": "",
        "cpassword": "",
    }
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    
    else:
        if request.method == "POST":
                fname = request.POST.get("fname")
                lname = request.POST.get("lname")
                email = request.POST.get("email")
                dob = request.POST.get("dob")
                password = request.POST.get("password")
                cpassword = request.POST.get("cpassword")
                
                context['fname'] = fname
                context['lname'] = lname
                context['email'] = email
                context['dob'] = dob
                context['password'] = password
                context['cpassword'] = cpassword

                if not email.isspace():
                    if User.objects.filter(email = email).first() :
                        messages.error(request, "An account already exists with this email")
                    else:
                        if (not fname.isspace()) and (not lname.isspace()) and (not password.isspace()) and (not cpassword.isspace()):
                            if check_str_special(fname) or check_str_special(lname):
                                messages.error(request, "Special charecters are not allowed")
                            else:
                                if password == cpassword:
                                    if request.recaptcha_is_valid:
                                        newUser = User.objects.create_user(email=email, password=password)
                                        newUser.first_name = fname
                                        newUser.last_name = lname
                                        newUser.save()
                                        
                                        request.session['user_email'] = email
                                        
                                        context['fname'] = context['lname'] = context['email'] = context['password'] = context['cpassword'] = ""
                        
                                        messages.success(request, "Account created successfully. Check your email for OTP")
                                        return redirect('email-verification')
                                else:
                                    messages.error(request, "Your passwords do not match")
                                
                        else:
                            messages.error(request, "All fields are required")
                else:
                    messages.error(request, "All fields are required")
    
    return render(request, './accounts/signin.html', context)


@check_recaptcha
def login(request):
    email = password = ""
    context = {
        "RECAPTCHA_PUBLIC_KEY" : RECAPTCHA_PUBLIC_KEY,
        "email": email,
        "password": password,
    }
    if request.session.get('user_email'):
        del request.session['user_email']
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    
    else:
        try:
            if request.method == "POST":
                email = request.POST.get("email")
                password = request.POST.get("password")
                
                context["email"] = email
                context["password"] = password
                
                if (not email.isspace()) and (not password.isspace()):
                    if request.recaptcha_is_valid:
                        try:
                            checkUser = User.objects.get(email=email)
                            user = auth.authenticate(email = email, password = password)
                            if user is not None:
                                if not checkUser.is_verified:                                
                                    messages.warning(request, "Your email is not verified. Please verify it")
                                
                                auth.login(request, user)
                                messages.success(request, "you are successfully logged in")
                                
                                context["email"] = context["password"] = ""
                                
                                if request.GET.get('next') != None:
                                    return redirect(request.GET.get('next'))
                                
                                return redirect('dashboard')
                            else:
                                messages.error(request, "Invalid credentials. Please check your email and password")
                        except User.DoesNotExist:
                            messages.error(request, "No account exists with this email address")  
                        except Exception as e:
                            print(e)
                            messages.error(request, "Something went wrong")  
                                        
                else:
                    messages.error(request, "Email and password are required")
            
        except Exception as e:
            print(e)
            messages.info(request, "Something went wrong")
        
    return render(request, './accounts/login.html', context)



@login_required(login_url="/auth/login")
def dashboard(request):
    fname = lname = dob = country = city = course = institute = ""
    searchHistory = course_searchHistory = topic_searchHistory = ""
    searchHistoryCount = course_searchHistoryCount = topic_searchHistoryCount = topicHistoryCount = courseHistoryCount = 0
    last_week = current_time - datetime.timedelta(days=7)
    context = {
        'fname': fname,
        'lname': lname,
        'dob': dob,
        'country': country,
        'city': city,
        'course': course,
        'institute': institute,

    }
    if not request.user.is_verified:
        messages.warning(request, "Your email is not verified it. Please verify it")
    
    try:
        getProfile = UserProfile.objects.get(user=request.user)
        dob = getProfile.date_of_birth
        city = getProfile.city
        country = getProfile.country
        course = getProfile.course_name
        institute = getProfile.institute_name
        
        '''Get user's data for statistics for last week'''
        #getting chatbot search
        search = UserRequestHistory.objects.filter(created_at__gte=last_week, chatroom__user=request.user)
        searchHistory = search.values('request').annotate(count=Count('request'))
        searchHistoryCount = search.count()
        
        #getting course and topic search
        course_topic_search = UserCourseHistory.objects.filter(created_at__gte=last_week, user=request.user)
        #getting course search
        course_searchHistory = course_topic_search.filter(type="subject").values('request').annotate(count=Count('request'))
        course_searchHistoryCount = course_searchHistory.count()
        
        #getting topic search
        topic_searchHistory = course_topic_search.filter(type="topic").values('request').annotate(count=Count('request'))
        topic_searchHistoryCount = topic_searchHistory.count()
        
        '''For pie graph'''
        courseHistoryCount = course_topic_search.filter(type="subject").count()
        topicHistoryCount = course_topic_search.filter(type="topic").count()
        
        '''Get users data for compairing'''
        previous_week = last_week - datetime.timedelta(days=7)
        #getting chat searches
        this_week_chat = searchHistoryCount
        previous_week_chat = UserRequestHistory.objects.filter(created_at__range=(previous_week, last_week), chatroom__user=request.user).count()
        
        #getting course and topic search
        previous_week_course_topic = UserCourseHistory.objects.filter(created_at__range=(previous_week, last_week), user=request.user)
        #getting course search
        this_week_course = course_topic_search.filter(type="subject").count()
        previous_week_course = previous_week_course_topic.filter(type="subject").count()
        
        #getting topic search
        this_week_topic = course_topic_search.filter(type="topic").count()
        previous_week_topic = previous_week_course_topic.filter(type="topic").count()
        
        if this_week_chat > 0:
            chat_percent = -int(((previous_week_chat-this_week_chat)/this_week_chat)*100)
        else:
            chat_percent = 0
        if this_week_course > 0:
            course_percent = -int(((previous_week_course-this_week_course)/this_week_course)*100)
        else:
            course_percent = 0
        if this_week_topic > 0:
            topic_percent = -int(((previous_week_topic-this_week_topic)/this_week_topic)*100)
        else:
            topic_percent = 0
               
        context["chat_percent"] = chat_percent
        context["course_percent"] = course_percent
        context["topic_percent"] = topic_percent

        chart_data = []
        check_date = last_week
        while (check_date <= current_time):
            data = [check_date, 0, 0, 0]
            chat_data = UserRequestHistory.objects.filter(created_at__date=check_date, chatroom__user=request.user).count()
            course_data = UserCourseHistory.objects.filter(created_at__date=check_date, type="subject", user=request.user).count()
            topic_data = UserCourseHistory.objects.filter(created_at__date=check_date, type="topic", user=request.user).count()
            
            data[1], data[2], data[3] = chat_data, course_data, topic_data
            chart_data.append(data)
            
            check_date += datetime.timedelta(days=1)
    
        context["chart_data"] = chart_data
        
    except Exception as e:
        getProfile = None
        print(e)
        
    try:
        if request.method == "POST":
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            dob = request.POST.get("dob")
            country = request.POST.get("country")
            city = request.POST.get("city")
            course = request.POST.get("course")
            institute = request.POST.get("institute")
            
            if check_str_special(fname) or check_str_special(lname) or check_str_special(country) or check_str_special(city) or check_str_special(course) or check_str_special(institute):
                messages.error(request, "Special charecters are not allowed")
            else:
                if getProfile is not None:
                    user = request.user
                    user.first_name = fname
                    user.last_name = lname
                    user.save()
                    
                    getProfile.city = city
                    getProfile.country = country
                    getProfile.course_name = course
                    getProfile.institute_name = institute
                    getProfile.save()
                    
                    messages.success(request, "Profile updated successfully")
                            
    except Exception as e:
        print(e)
    
    context["fname"] = request.user.first_name
    context["lname"] = request.user.last_name
    context["dob"] = dob
    context["city"] = city
    context["country"] = country
    context["course"] = course
    context["institute"] = institute
    
    context["last_week"] = last_week
    context["searchHistory"] = searchHistory
    context["searchHistoryCount"] = searchHistoryCount
    context["course_searchHistory"] = course_searchHistory
    context["course_searchHistoryCount"] = course_searchHistoryCount
    context["topic_searchHistory"] = topic_searchHistory
    context["topic_searchHistoryCount"] = topic_searchHistoryCount
    
    context["courseHistoryCount"] = courseHistoryCount
    context["topicHistoryCount"] = topicHistoryCount
    
        
    return render(request, './accounts/dashboard.html', context)



def email_verification(request):
    email = otp = ""
    context = {
        'email': email,
        'otp': otp
    }

    try: 
        if request.session.get('user_email'):
            email = request.session.get('user_email')
            
        elif request.user.is_authenticated:
            email = request.user.email   
            if request.user.is_verified:
                messages.warning(request, "Your email is already verified")
                return redirect('dashboard')
        
                   
        if request.method == "POST" and "send-otp" in request.POST:
            email = request.POST.get("email")
            email = email.strip()
                            
            if not email.isspace():
                
                try:
                    getUser = User.objects.get(email=email)
                    newOTP = OTP(user=getUser)
                    newOTP.save()
                    
                    request.session["user_email"] = email
                    messages.info(request, f"OTP has been send to your email {email}")
                    
                except User.DoesNotExist:
                    messages.error(request, "No account exists with this email address")  
                except Exception as e:
                    print(e)
                    messages.error(request, "Something went wrong")  
                
            else:
                messages.error(request, "Email is required")

        elif request.method == "POST" and "verify-email" in request.POST:
            otp = request.POST.get("otp")
            otp = otp.strip()
            
            if not otp.isspace():
                if otp.isnumeric():
                    try:
                        if request.user.is_authenticated:
                            getUser = request.user
                        else:
                            getUser = User.objects.get(email=email)
                        if not getUser.is_verified:
                            ten_min_ago = current_time - datetime.timedelta(minutes=10)
                            checkOTP = OTP.objects.filter(otp=otp, user=getUser, is_expired=False, purpose="email_verification", created_at__gte=ten_min_ago).first()
                            if checkOTP:
                                getUser.is_verified = True
                                getUser.save()
                                
                                checkOTP.is_expired = True
                                checkOTP.save()
                                messages.success(request, "Email verified successfully.")
                                
                                if request.session.get('user_email'):
                                    del request.session['user_email']
                                
                                if request.user.is_authenticated:
                                    return redirect('dashboard')
                                
                                return redirect('login')
                            else:
                                messages.error(request, "Invalid OTP. OTP may get expired")
                        else:
                            messages.warning(request, "This account is already verified")
                            return redirect('login')
                    except User.DoesNotExist:
                        messages.error(request, "No account exists with this email address")  
                    except Exception as e:
                        print(e)
                        messages.error(request, "Something went wrong")
                else:
                    messages.error(request, "Invalid otp")
                     
                    
            else:
                messages.error(request, "OTP is required")

    except Exception as e:
        print(e)
        

    context['email'] = email
    context['otp'] = otp
    
    return render(request, './accounts/email-verification.html')



def reset_password(request):
    email = otp = password = cpassword = ""
    context = {
        'email' : email,
        'otp': otp,
        'password' : password,
        'cpassword' : cpassword,
    }
    
    try:
        if request.session.get('user_email'):
            email = request.session.get('user_email')
        elif request.user.is_authenticated:
            email = request.user.email
            
        if request.method == "POST" and "send-otp" in request.POST:
            email = request.POST.get("email")
            if not email.isspace():
                try:
                    getUser = User.objects.get(email=email)
                    newOTP = OTP(user=getUser, purpose="reset_password")
                    newOTP.save()
                    
                    request.session["user_email"] = email
                    messages.info(request, f"OTP has been send to you email {email}")
                    
                except User.DoesNotExist:
                    messages.error(request, "No account exists with this email address")  
                except Exception as e:
                    print(e)
                    messages.error(request, "Something went wrong")  

            else:
                messages.error(request, "Email is required")
                
        elif request.method == "POST" and "verify-email" in request.POST:
            otp = request.POST.get("otp")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            
            if (not otp.isspace()) and (not password.isspace()) and (not cpassword.isspace()):
                if otp.isnumeric():
                    if password == cpassword:                    
                        try:
                            getUser = User.objects.get(email=email)
                            ten_min_ago = current_time - datetime.timedelta(minutes=10)
                            checkOTP = OTP.objects.filter(otp=otp, user=getUser, is_expired=False, purpose="reset_password", created_at__gte=ten_min_ago).first()
                            if checkOTP:                        
                                checkOTP.is_expired = True
                                checkOTP.save()
                                
                                getUser.set_password(password)
                                getUser.save()
                                
                                messages.success(request, "Password reset successfull. Now please login")
                                return redirect('login')

                            else:
                                messages.error(request, "Invalid OTP. OTP may get expired")
                                
                        except User.DoesNotExist:
                            messages.error(request, "No account exists with this email address")  
                        except Exception as e:
                            print(e)
                            messages.error(request, "Something went wrong")  
                        
                    else:
                        messages.error(request, "Passwords do not match")
                else:
                    messages.error(request, "Invalid OTP")
            
            else:
                messages.error(request, "OTP, Passwords are required")
        
    except Exception as e:
        print(e)
        
    context['email'] = email
    context['otp'] = otp
    context['password'] = password
    context['cpassword'] = cpassword
    
    return render(request, './accounts/reset-password.html', context)



@login_required(login_url="/auth/login")
def logout(request):
    if request.session.get('user_email'):
        del request.session['user_email']
    
    request.user.last_logout = current_time
    request.user.save()
    auth.logout(request)  
    messages.warning(request, "You are logged out now")  
    return redirect('login')





        