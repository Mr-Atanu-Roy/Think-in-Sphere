from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User, OTP, UserProfile
from accounts.utils import current_time

import datetime


# Create your views here.
def signin(request):
    context = {
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

                if email != "":
                    if User.objects.filter(email = email).first() :
                        messages.error(request, "An account already exists with this email")
                    else:
                        if fname != "" and lname != "" and email != "" and password != "" and cpassword != "":
                            if password == cpassword:
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



def login(request):
    email = password = ""
    context = {
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
                
                if email != "" and password != "":
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
            email = email.lstrip()
            email = email.rstrip()
                            
            if email != "":
                
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
            otp = otp.lstrip()
            otp = otp.rstrip()
            
            if otp != "":
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
            if email != "":
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
            
            if otp != "" and password !="" and cpassword != "":
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